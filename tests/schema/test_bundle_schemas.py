from __future__ import annotations

import shutil
import tempfile
import unittest
from pathlib import Path

from src.common.schema_validator import validate_file
from src.common.stub_runner import run_manifest


class TestBundleSchemas(unittest.TestCase):
    def setUp(self) -> None:
        self.repo_root = Path(__file__).resolve().parents[2]
        self.tmpdir = tempfile.TemporaryDirectory()
        self.work_root = Path(self.tmpdir.name) / "eas-scalar-field-testbed"
        shutil.copytree(self.repo_root, self.work_root, dirs_exist_ok=True)
        self.manifest = self.work_root / "experiments" / "motif_variation" / "electron_baseline_variation_v2.yaml"

    def tearDown(self) -> None:
        self.tmpdir.cleanup()

    def _run_and_paths(self) -> dict[str, Path]:
        result = run_manifest(self.manifest, repo_root=self.work_root)
        return {k: Path(v) for k, v in result.items()}

    def test_resolved_manifest_schema(self) -> None:
        paths = self._run_and_paths()
        validate_file(paths["resolved_manifest_path"], self.work_root / "schemas" / "resolved_manifest.schema.json")

    def test_registry_record_schema(self) -> None:
        paths = self._run_and_paths()
        validate_file(paths["registry_record_path"], self.work_root / "schemas" / "registry_record.schema.json")

    def test_result_summary_schema(self) -> None:
        paths = self._run_and_paths()
        validate_file(paths["summary_json_path"], self.work_root / "schemas" / "result_summary.schema.json")

    def test_artifact_index_schema(self) -> None:
        paths = self._run_and_paths()
        validate_file(paths["artifact_index_path"], self.work_root / "schemas" / "artifact_index.schema.json")


if __name__ == "__main__":
    unittest.main()
