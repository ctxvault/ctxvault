#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path
import shutil
import sys
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[1]
SRC_ROOT = REPO_ROOT / "src"
if str(SRC_ROOT) not in sys.path:
    sys.path.insert(0, str(SRC_ROOT))

from ctxvault.core import CtxVault
from ctxvault.layout import default_layout
from ctxvault.surface import CtxVaultSurface


DEFAULT_ROOT = Path("/tmp/ctxvault-v040-trial")
DEFAULT_SOURCE_PATH = REPO_ROOT / "fixtures" / "v0.3.4-context-extract" / "markdown-vault"
WORKSTREAM_ID = "ws_20260421_ctxvault_schema"
WORKSTREAM_REF = f"workstream://{WORKSTREAM_ID}"
PREPARE_QUERY = "stable one click extraction privacy projection receipts"


def run_trial(*, root: Path, source_path: Path, reset: bool = False) -> dict[str, Any]:
    root = root.resolve()
    source_path = source_path.resolve()
    if reset:
        _safe_reset(root)

    surface = CtxVaultSurface(CtxVault(default_layout(root)))
    surface.vault.initialize()
    surface.vault.import_core_fixtures(REPO_ROOT / "fixtures" / "core")

    dry_run = surface.context_extract(
        source_paths=[source_path],
        source_kind="markdown-vault",
        scope_kind="project",
        scope_value="ctxvault",
        recursive=True,
        prepare_query=PREPARE_QUERY,
        workstream_ref=WORKSTREAM_REF,
        project_targets=["workstream-brief"],
        workstream_id=WORKSTREAM_ID,
        dry_run=True,
    )
    run = surface.context_extract(
        source_paths=[source_path],
        source_kind="markdown-vault",
        scope_kind="project",
        scope_value="ctxvault",
        recursive=True,
        prepare_query=PREPARE_QUERY,
        workstream_ref=WORKSTREAM_REF,
        project_targets=["workstream-brief"],
        workstream_id=WORKSTREAM_ID,
    )
    inspection = surface.receipt_inspect(receipt_path=Path(str(run["receipt_path"])))
    doctor = surface.doctor_report()
    doctor_checks = {check["name"]: check for check in doctor["checks"]}
    pass_checks = {
        "dry_run_writes_plan_without_imports": dry_run["status"] == "dry_run" and not dry_run["imports"],
        "local_sources_imported": any(int(item.get("receipt_count") or 0) > 0 for item in run["imports"]),
        "projection_gated_by_handoff_ready": bool(run["prepare"].get("handoff_ready")) and len(run["projections"]) == 1,
        "receipt_chain_inspects": inspection["status"] == "pass" and not inspection["chains"][0]["missing_links"],
        "doctor_extract_checks_pass": doctor_checks["context_extract_receipts"]["status"] == "pass"
        and doctor_checks["projection_selection_receipts"]["status"] == "pass",
    }
    projection_paths = [str(projection.get("output_path")) for projection in run.get("projections") or []]
    status = "pass" if run["status"] == "pass" and all(pass_checks.values()) else "fail"
    summary = {
        "schema_id": "ctxvault.v0.4.0-context-handoff-trial/v1",
        "status": status,
        "root": str(root),
        "source_path": str(source_path),
        "source_kind": "markdown-vault",
        "operation": "local_sources_to_reviewed_context_to_receipt_backed_handoff",
        "prepare_query": PREPARE_QUERY,
        "workstream_ref": WORKSTREAM_REF,
        "pass_checks": pass_checks,
        "receipt_path": run["receipt_path"],
        "receipt_inspection_status": inspection["status"],
        "doctor_status": doctor["status"],
        "selected_slice_refs": run["prepare"].get("selected_slice_refs"),
        "projection_output_paths": projection_paths,
        "next_actions": run["next_actions"],
    }
    summary_path = root / "artifacts" / "v0.4.0-context-handoff-trial-summary.json"
    summary_path.parent.mkdir(parents=True, exist_ok=True)
    summary["summary_path"] = str(summary_path)
    summary["scorecard_path"] = str(summary_path)
    summary_path.write_text(json.dumps(summary, ensure_ascii=True, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return summary


def _safe_reset(root: Path) -> None:
    resolved = root.resolve()
    tmp_root = Path("/tmp").resolve()
    if tmp_root not in resolved.parents or not resolved.name.startswith("ctxvault-"):
        raise ValueError("--reset only accepts ctxvault-* roots under the system temporary directory")
    if resolved.exists():
        shutil.rmtree(resolved)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Run the v0.4.0 local context handoff trial: local sources -> reviewed context -> receipt-backed handoff."
    )
    parser.add_argument("--root", type=Path, default=DEFAULT_ROOT, help="Vault/output root for the v0.4.0 trial.")
    parser.add_argument(
        "--source-path",
        type=Path,
        default=DEFAULT_SOURCE_PATH,
        help="Local source path to import for the trial. Defaults to the repo-contained Markdown vault fixture.",
    )
    parser.add_argument("--reset", action="store_true", help="Delete an existing /tmp/ctxvault-* trial root before running.")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    summary = run_trial(root=args.root, source_path=args.source_path, reset=args.reset)
    print(json.dumps(summary, ensure_ascii=True, indent=2, sort_keys=True))
    return 0 if summary["status"] == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
