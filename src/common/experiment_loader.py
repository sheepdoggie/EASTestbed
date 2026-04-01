from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

from .schema_validator import load_document, validate_file


@dataclass(frozen=True)
class LoadedExperiment:
    repo_root: Path
    manifest_path: Path
    manifest: dict[str, Any]
    schema_path: Path


def infer_repo_root(manifest_path: Path) -> Path:
    """Infer the repository root from a manifest path.

    Expected layout: <repo>/experiments/<family>/<manifest>.yaml
    """
    resolved = manifest_path.resolve()
    for parent in resolved.parents:
        if (parent / "schemas").exists() and (parent / "standards").exists():
            return parent
    raise FileNotFoundError(
        f"Could not infer repository root from {manifest_path}; expected schemas/ and standards/ directories."
    )


def resolve_schema_path(repo_root: Path, manifest: dict[str, Any]) -> Path:
    schema_ref = manifest.get("schema_ref") or "schemas/experiment.schema.json"
    schema_path = (repo_root / schema_ref).resolve()
    if not schema_path.exists():
        raise FileNotFoundError(f"Schema file not found: {schema_path}")
    return schema_path


def load_experiment(manifest_path: str | Path, validate: bool = True) -> LoadedExperiment:
    path = Path(manifest_path).resolve()
    manifest = load_document(path)
    if not isinstance(manifest, dict):
        raise TypeError(f"Experiment manifest at {path} must parse to an object/dictionary")

    repo_root = infer_repo_root(path)
    schema_path = resolve_schema_path(repo_root, manifest)

    if validate:
        validate_file(path, schema_path)

    return LoadedExperiment(
        repo_root=repo_root,
        manifest_path=path,
        manifest=manifest,
        schema_path=schema_path,
    )
