from __future__ import annotations

import shutil
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from src.common.schema_validator import SchemaValidationError
from src.common.stub_runner import run_manifest


class TestRunnerFailsOnInvalidBundle(unittest.TestCase):
    def setUp(self) -> None:
        self.repo_root = Path(__file__).resolve().parents[2]
        self.tmpdir = tempfile.TemporaryDirectory()
        self.work_root = Path(self.tmpdir.name) / "eas-scalar-field-testbed"
        shutil.copytree(self.repo_root, self.work_root, dirs_exist_ok=True)
        self.manifest = self.work_root / "experiments" / "motif_variation" / "electron_baseline_variation_v2.yaml"

    def tearDown(self) -> None:
        self.tmpdir.cleanup()

    def test_runner_raises_on_invalid_result_summary(self) -> None:
        def bad_summary(*args, **kwargs):
            return {
                "summary_version": "1.0",
                "experiment_id": "bad",
                "status": "stub_completed",
                "computed_at_utc": "now",
                "module_versions": {},
                "artifacts": {},
                "summary": {
                    "kind": "stub"
                }
            }

        with patch("src.common.stub_runner.build_result_summary", side_effect=bad_summary):
            with self.assertRaises(SchemaValidationError):
                run_manifest(self.manifest, repo_root=self.work_root)


if __name__ == "__main__":
    unittest.main()
