from __future__ import annotations

from contextlib import closing
from datetime import datetime, timezone
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
        for table in ["object_index", "workstreams", "memory_candidates", "prompt_patches", "context_bundles"]:
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


def _utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()
