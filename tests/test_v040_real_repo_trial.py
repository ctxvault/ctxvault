from __future__ import annotations

import json
from pathlib import Path
import subprocess
import sys
from tempfile import TemporaryDirectory
import unittest


ROOT = Path(__file__).resolve().parents[1]


class V040RealRepoTrialTests(unittest.TestCase):
    def test_real_repo_trial_builds_bounded_source_packet_and_report(self) -> None:
        with TemporaryDirectory() as repo_dir, TemporaryDirectory() as root_dir:
            repo = Path(repo_dir)
            trial_root = Path(root_dir)
            (repo / "README.md").write_text(
                "# Sample Tool\n\n"
                "Sample Tool is a local developer utility with deterministic setup.\n",
                encoding="utf-8",
            )
            (repo / "docs").mkdir()
            (repo / "docs" / "usage.md").write_text(
                "# Usage\n\nRun the CLI locally before handing context to an AI assistant.\n",
                encoding="utf-8",
            )
            (repo / "package.json").write_text('{"name": "sample-tool"}\n', encoding="utf-8")

            result = subprocess.run(
                [
                    sys.executable,
                    str(ROOT / "scripts" / "run_v040_real_repo_trial.py"),
                    "--repo",
                    str(repo),
                    "--root",
                    str(trial_root),
                    "--max-files",
                    "3",
                    "--max-bytes-per-file",
                    "1000",
                ],
                check=False,
                capture_output=True,
                text=True,
            )

            self.assertEqual(result.returncode, 0, msg=result.stderr)
            payload = json.loads(result.stdout)
            self.assertEqual(payload["schema_id"], "ctxvault.v0.4.0-real-repo-trial/v1")
            self.assertEqual(payload["status"], "pass")
            self.assertTrue(all(payload["pass_checks"].values()))
            self.assertTrue(Path(payload["trial_report_path"]).exists())
            self.assertTrue(Path(payload["summary_path"]).exists())
            self.assertTrue(payload["source_packet"]["contains_source_excerpts"])
            self.assertTrue(payload["source_packet"]["operator_review_required_before_sharing"])
            self.assertIn("README.md", {item["relative_path"] for item in payload["source_packet"]["selected_files"]})
            self.assertTrue(payload["projection_output_paths"])
            self.assertTrue(payload["public_claim_boundary"]["no_provider_call"])
            self.assertTrue(payload["public_claim_boundary"]["no_runtime_control"])
            self.assertIn("not_done", payload["receipt_explanation"]["states"])


if __name__ == "__main__":
    unittest.main()
