from __future__ import annotations

import argparse
import sys
from pathlib import Path

from src.common.stub_runner import run_manifest


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="python -m src.common.run_experiment",
        description="Run a manifest-driven EAS Scalar-Field Testbed experiment.",
    )
    parser.add_argument(
        "manifest",
        type=Path,
        help="Path to the experiment manifest YAML or JSON file.",
    )
    parser.add_argument(
        "--repo-root",
        type=Path,
        default=None,
        help=(
            "Optional repository root. If omitted, the runner will infer it from "
            "the manifest location."
        ),
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    manifest_path = args.manifest.expanduser().resolve()
    repo_root = args.repo_root.expanduser().resolve() if args.repo_root else None

    if not manifest_path.exists():
        parser.error(f"manifest does not exist: {manifest_path}")

    try:
        result = run_manifest(manifest_path=manifest_path, repo_root=repo_root)
    except Exception as exc:  # pragma: no cover - defensive CLI boundary
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1

    record_path = result.get("registry_record_path")
    print("Experiment completed successfully.")
    if record_path:
        print(f"Registry record: {record_path}")
    else:
        print("Registry record path not returned by runner.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
