from __future__ import annotations

from contextlib import closing
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import sqlite3
from typing import Any

from .adapters import projection_adapter_healthcheck
from .layout import default_layout


DOCTOR_SCHEMA_ID = "ctxvault.doctor-report/v1"


def build_doctor_report(root: Path, *, project_root: Path | None = None) -> dict[str, Any]:
    resolved_root = root.resolve()
    repo_root = (project_root or Path(__file__).resolve().parents[2]).resolve()
    layout = default_layout(resolved_root)
    checks = [
        _path_check("vault.sqlite", layout.sqlite_path, required=False),
        _sqlite_counts_check(layout.sqlite_path),
        _json_file_check("protection_policy_fixture", repo_root / "fixtures" / "controls" / "protection-policy.json"),
        _json_file_check("backup_receipt_fixture", repo_root / "fixtures" / "controls" / "backup-check-receipt.json"),
        _json_file_check("context_injection_launch_gate", repo_root / "release" / "context-injection-m1-launch-gate.json"),
        _experimental_compiled_state_check(repo_root),
        _context_slice_contract_check(repo_root),
        _context_slice_index_check(layout.sqlite_path),
        _projection_slice_refs_check(layout.sqlite_path, resolved_root),
        _adapter_check("agents-md", root=resolved_root),
        _adapter_check("claude-md", root=resolved_root),
        _adapter_check("workstream-brief", root=resolved_root),
    ]
    status = "pass"
    if any(check["status"] == "fail" for check in checks):
        status = "fail"
    elif any(check["status"] == "warn" for check in checks):
        status = "warn"
    return {
        "schema_id": DOCTOR_SCHEMA_ID,
        "generated_at": _utc_now(),
        "root": str(resolved_root),
        "mode": "read_only",
        "status": status,
        "summary": {
            "pass": sum(1 for check in checks if check["status"] == "pass"),
            "warn": sum(1 for check in checks if check["status"] == "warn"),
            "fail": sum(1 for check in checks if check["status"] == "fail"),
        },
        "checks": checks,
    }


def _path_check(name: str, path: Path, *, required: bool) -> dict[str, Any]:
    exists = path.exists()
    return {
        "name": name,
        "status": "pass" if exists else ("fail" if required else "warn"),
        "detail": str(path),
        "read_only": True,
    }


def _json_file_check(name: str, path: Path) -> dict[str, Any]:
    if not path.exists():
        return {"name": name, "status": "fail", "detail": f"missing {path}", "read_only": True}
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        return {"name": name, "status": "fail", "detail": f"invalid JSON: {exc}", "read_only": True}
    if not isinstance(payload, dict):
        return {"name": name, "status": "fail", "detail": "expected JSON object", "read_only": True}
    return {"name": name, "status": "pass", "detail": str(path), "read_only": True}


def _sqlite_counts_check(sqlite_path: Path) -> dict[str, Any]:
    if not sqlite_path.exists():
        return {
            "name": "index_counts",
            "status": "warn",
            "detail": "vault index has not been initialized",
            "read_only": True,
            "counts": {},
        }
    counts: dict[str, int] = {}
    with closing(sqlite3.connect(sqlite_path)) as conn:
        for table in ["object_index", "workstreams", "memory_candidates", "prompt_patches", "context_bundles", "context_slices"]:
            exists = conn.execute(
                "SELECT 1 FROM sqlite_master WHERE type = 'table' AND name = ?",
                (table,),
            ).fetchone()
            if exists is None:
                counts[table] = 0
                continue
            row = conn.execute(f"SELECT COUNT(*) FROM {table}").fetchone()
            counts[table] = int(row[0]) if row is not None else 0
    return {
        "name": "index_counts",
        "status": "pass",
        "detail": str(sqlite_path),
        "read_only": True,
        "counts": counts,
    }


def _context_slice_contract_check(repo_root: Path) -> dict[str, Any]:
    schema_path = repo_root / "docs" / "v0.3.1-local-safety" / "experimental-schemas" / "ctxvault-context-slice-v1.schema.json"
    fixture_path = repo_root / "docs" / "v0.3.1-local-safety" / "experimental-fixtures" / "context-slice.json"
    if not schema_path.exists() or not fixture_path.exists():
        return {
            "name": "context_slice_contract",
            "status": "fail",
            "detail": "experimental schema or fixture is missing",
            "read_only": True,
        }
    try:
        schema = json.loads(schema_path.read_text(encoding="utf-8"))
        fixture = json.loads(fixture_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        return {
            "name": "context_slice_contract",
            "status": "fail",
            "detail": f"invalid JSON: {exc}",
            "read_only": True,
        }
    status = "pass" if fixture.get("schema_id") == "ctxvault.context-slice/v1" and schema.get("title") else "fail"
    return {
        "name": "context_slice_contract",
        "status": status,
        "detail": str(schema_path),
        "read_only": True,
        "fixture_path": str(fixture_path),
    }


def _context_slice_index_check(sqlite_path: Path) -> dict[str, Any]:
    if not sqlite_path.exists():
        return {
            "name": "context_slice_index",
            "status": "warn",
            "detail": "vault index has not been initialized",
            "read_only": True,
            "slice_count": 0,
            "stale_source_count": 0,
            "repair_hint": "run ctxvault context-slice-rebuild after importing source objects",
        }
    with closing(sqlite3.connect(sqlite_path)) as conn:
        conn.row_factory = sqlite3.Row
        has_slices = _sqlite_has_table(conn, "context_slices")
        has_fts = _sqlite_has_table(conn, "context_slice_fts")
        if not has_slices:
            return {
                "name": "context_slice_index",
                "status": "warn",
                "detail": "context_slices table is missing; run context-slice-rebuild",
                "read_only": True,
                "slice_count": 0,
                "stale_source_count": 0,
                "repair_hint": "run ctxvault context-slice-rebuild",
            }
        slice_count = int(conn.execute("SELECT COUNT(*) FROM context_slices").fetchone()[0])
        source_count = _context_slice_source_count(conn)
        privacy_counts = {
            str(row["privacy_class"]): int(row["count"])
            for row in conn.execute(
                """
                SELECT privacy_class, COUNT(*) AS count
                FROM context_slices
                GROUP BY privacy_class
                ORDER BY privacy_class ASC
                """
            ).fetchall()
        }
        stale_source_count = _stale_context_slice_source_count(conn)
    status = "pass"
    details: list[str] = []
    if not has_fts:
        status = "warn"
        details.append("context_slice_fts table is missing")
    if source_count > 0 and slice_count == 0:
        status = "warn"
        details.append("slice index is empty while sliceable sources exist")
    if stale_source_count > 0:
        status = "warn"
        details.append(f"{stale_source_count} source(s) changed after slice rebuild")
    return {
        "name": "context_slice_index",
        "status": status,
        "detail": "; ".join(details) if details else str(sqlite_path),
        "read_only": True,
        "slice_count": slice_count,
        "sliceable_source_count": source_count,
        "stale_source_count": stale_source_count,
        "privacy_counts": privacy_counts,
        "repair_hint": "run ctxvault context-slice-rebuild" if status == "warn" else None,
    }


def _projection_slice_refs_check(sqlite_path: Path, root: Path) -> dict[str, Any]:
    receipt_refs = _projection_receipt_slice_refs(root)
    selected_slice_refs = sorted({ref for item in receipt_refs for ref in item["selected_slice_refs"]})
    if not selected_slice_refs:
        return {
            "name": "projection_slice_refs",
            "status": "pass",
            "detail": "no projection receipts reference context slices",
            "read_only": True,
            "projection_receipt_count": 0,
            "missing_slice_refs": [],
        }
    if not sqlite_path.exists():
        return {
            "name": "projection_slice_refs",
            "status": "warn",
            "detail": "projection receipts reference context slices but the slice index is missing",
            "read_only": True,
            "projection_receipt_count": len(receipt_refs),
            "missing_slice_refs": selected_slice_refs,
            "repair_hint": "run ctxvault context-slice-rebuild or logical-purge-plan --include-projections before clearing projection outputs",
        }
    with closing(sqlite3.connect(sqlite_path)) as conn:
        conn.row_factory = sqlite3.Row
        if not _sqlite_has_table(conn, "context_slices"):
            existing_refs: set[str] = set()
        else:
            placeholders = ",".join("?" for _ in selected_slice_refs)
            rows = conn.execute(
                f"SELECT slice_ref FROM context_slices WHERE slice_ref IN ({placeholders})",
                selected_slice_refs,
            ).fetchall()
            existing_refs = {str(row["slice_ref"]) for row in rows}
    missing = [ref for ref in selected_slice_refs if ref not in existing_refs]
    return {
        "name": "projection_slice_refs",
        "status": "warn" if missing else "pass",
        "detail": (
            f"{len(missing)} selected slice ref(s) are absent from the current slice index"
            if missing
            else "projection slice refs are present in the current slice index"
        ),
        "read_only": True,
        "projection_receipt_count": len(receipt_refs),
        "missing_slice_refs": missing,
        "repair_hint": (
            "run ctxvault context-slice-rebuild or logical-purge-plan --include-projections before clearing projection outputs"
            if missing
            else None
        ),
    }


def _experimental_compiled_state_check(repo_root: Path) -> dict[str, Any]:
    schema_path = repo_root / "docs" / "v0.3-compiled-context" / "experimental-schemas" / "ctxvault-compiled-workstream-state-v1.schema.json"
    fixture_path = repo_root / "docs" / "v0.3-compiled-context" / "experimental-fixtures" / "compiled-workstream-state.json"
    if not schema_path.exists() or not fixture_path.exists():
        return {
            "name": "compiled_workstream_state_contract",
            "status": "fail",
            "detail": "experimental schema or fixture is missing",
            "read_only": True,
        }
    try:
        schema = json.loads(schema_path.read_text(encoding="utf-8"))
        fixture = json.loads(fixture_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        return {
            "name": "compiled_workstream_state_contract",
            "status": "fail",
            "detail": f"invalid JSON: {exc}",
            "read_only": True,
        }
    status = "pass" if fixture.get("schema_id") == "ctxvault.compiled-workstream-state/v1" and schema.get("title") else "fail"
    return {
        "name": "compiled_workstream_state_contract",
        "status": status,
        "detail": str(fixture_path),
        "read_only": True,
    }


def _adapter_check(target_kind: str, *, root: Path) -> dict[str, Any]:
    try:
        health = projection_adapter_healthcheck(root=root, target_kind=target_kind)
    except Exception as exc:  # pragma: no cover - defensive report path
        return {
            "name": f"adapter_healthcheck:{target_kind}",
            "status": "fail",
            "detail": str(exc),
            "read_only": True,
        }
    return {
        "name": f"adapter_healthcheck:{target_kind}",
        "status": "pass" if health.get("status") == "pass" else "warn",
        "detail": str(health.get("adapter_id") or target_kind),
        "read_only": True,
    }


def _projection_receipt_slice_refs(root: Path) -> list[dict[str, Any]]:
    receipts: list[dict[str, Any]] = []
    roots = [
        root / "exports" / "receipts",
        root / "artifacts",
        root / "receipts",
        root / ".ctxvault",
    ]
    for receipt_root in roots:
        if not receipt_root.exists():
            continue
        for path in sorted(receipt_root.rglob("*.json")):
            try:
                payload = json.loads(path.read_text(encoding="utf-8"))
            except (OSError, UnicodeDecodeError, json.JSONDecodeError):
                continue
            if not isinstance(payload, dict) or payload.get("schema_version") != "ctxvault.projection-receipt/v1":
                continue
            refs = _string_list(payload.get("selected_slice_refs"))
            preflight = payload.get("privacy_preflight") if isinstance(payload.get("privacy_preflight"), dict) else {}
            refs.extend(_string_list(preflight.get("selected_slice_refs")))
            refs = _unique(refs)
            if refs:
                receipts.append({"receipt_path": str(path.resolve()), "selected_slice_refs": refs})
    return receipts


def _utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def _sqlite_has_table(conn: sqlite3.Connection, table: str) -> bool:
    return (
        conn.execute(
            "SELECT 1 FROM sqlite_master WHERE type = 'table' AND name = ?",
            (table,),
        ).fetchone()
        is not None
    )


def _context_slice_source_count(conn: sqlite3.Connection) -> int:
    if not _sqlite_has_table(conn, "object_index"):
        return 0
    return int(
        conn.execute(
            """
            SELECT COUNT(*)
            FROM object_index
            WHERE object_kind IN ('knowledge_artifact', 'turn', 'episode', 'workstream')
            """
        ).fetchone()[0]
    )


def _stale_context_slice_source_count(conn: sqlite3.Connection) -> int:
    if not _sqlite_has_table(conn, "object_index"):
        return 0
    stale = 0
    rows = conn.execute(
        """
        SELECT DISTINCT source_ref, source_object_kind, source_content_sha256
        FROM context_slices
        WHERE source_object_kind IN ('knowledge_artifact', 'turn', 'episode')
        """
    ).fetchall()
    for row in rows:
        source_ref = str(row["source_ref"])
        source_kind = str(row["source_object_kind"])
        source_id = source_ref.split("://", 1)[1] if "://" in source_ref else source_ref
        object_kind = "knowledge_artifact" if source_kind == "knowledge_artifact" else source_kind
        object_row = conn.execute(
            """
            SELECT storage_path
            FROM object_index
            WHERE object_kind = ? AND object_id = ?
            """,
            (object_kind, source_id),
        ).fetchone()
        if object_row is None:
            stale += 1
            continue
        try:
            payload = json.loads(Path(str(object_row["storage_path"])).read_text(encoding="utf-8"))["payload"]
        except (OSError, KeyError, json.JSONDecodeError, TypeError):
            stale += 1
            continue
        current_sha = _source_content_sha(source_kind, payload)
        if current_sha != str(row["source_content_sha256"]):
            stale += 1
    return stale


def _source_content_sha(source_kind: str, payload: dict[str, Any]) -> str:
    if source_kind == "knowledge_artifact":
        content = payload.get("body")
    elif source_kind == "turn":
        content = payload.get("content")
    else:
        parts = [
            str(payload.get("title") or "").strip(),
            str(payload.get("summary") or "").strip(),
            str(payload.get("outcome") or "").strip(),
            " ".join(str(item).strip() for item in payload.get("key_points", []) if str(item).strip()),
        ]
        content = "\n".join(part for part in parts if part)
    if not isinstance(content, str):
        content = json.dumps(content, ensure_ascii=True, sort_keys=True)
    return hashlib.sha256(content.encode("utf-8")).hexdigest()


def _string_list(value: Any) -> list[str]:
    if not isinstance(value, list):
        return []
    return [str(item).strip() for item in value if str(item).strip()]


def _unique(values: list[str]) -> list[str]:
    seen: set[str] = set()
    result: list[str] = []
    for value in values:
        if value in seen:
            continue
        seen.add(value)
        result.append(value)
    return result
