from __future__ import annotations

import csv
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from .experiment_loader import LoadedExperiment, load_experiment
from .schema_validator import load_schema, validate_document, validate_file


def _slugify(value: str) -> str:
    return "".join(ch if ch.isalnum() or ch in {"-", "_", "."} else "_" for ch in value)


def _sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _manifest_hash(path: Path) -> str:
    return _sha256_bytes(path.read_bytes())


def _rel(path: Path, root: Path) -> str:
    return str(path.resolve().relative_to(root.resolve()))


def _timestamp() -> str:
    return datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")


def _utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def _default_paths(loaded: LoadedExperiment, experiment_id: str) -> dict[str, Path]:
    safe = _slugify(experiment_id)
    exp_dir = loaded.repo_root / "registry" / "experiments" / safe
    res_dir = loaded.repo_root / "registry" / "results" / safe
    art_dir = loaded.repo_root / "registry" / "artifacts" / safe
    rep_path = loaded.repo_root / "registry" / "reports" / f"{safe}.md"
    return {
        "experiment_dir": exp_dir,
        "results_dir": res_dir,
        "artifacts_dir": art_dir,
        "report_path": rep_path,
    }


def _load_output_schema(repo_root: Path, filename: str) -> dict[str, Any]:
    return load_schema(repo_root / "schemas" / filename)


def _module_versions(manifest: dict[str, Any]) -> dict[str, Any]:
    return {
        "motif_ref": manifest.get("motif", {}).get("motif_ref"),
        "field_ref": manifest.get("field_family", {}).get("field_ref"),
        "rule_ref": manifest.get("kernel_rule", {}).get("rule_ref"),
        "template_refs": manifest.get("templates", []),
        "invariant_refs": manifest.get("invariants", []),
        "redescription_ref": manifest.get("redescription", {}).get("engine_ref"),
        "interface_ref": manifest.get("interface", {}).get("emulator_ref") if manifest.get("interface", {}).get("enabled") else None,
        "schema_version": manifest.get("schema_version"),
    }


def build_resolved_manifest(loaded: LoadedExperiment) -> dict[str, Any]:
    manifest = loaded.manifest
    return {
        "record_version": "1.0",
        "experiment_id": manifest["experiment_id"],
        "title": manifest.get("title", manifest["experiment_id"]),
        "experiment_class": manifest["experiment_class"],
        "schema_version": manifest.get("schema_version"),
        "schema_path": _rel(loaded.schema_path, loaded.repo_root),
        "manifest_path": _rel(loaded.manifest_path, loaded.repo_root),
        "resolved_at_utc": _utc_now_iso(),
        "repo_root": str(loaded.repo_root.resolve()),
        "manifest": manifest,
    }


def build_result_summary(loaded: LoadedExperiment, bundle_paths: dict[str, Path]) -> dict[str, Any]:
    manifest = loaded.manifest
    return {
        "summary_version": "1.0",
        "experiment_id": manifest["experiment_id"],
        "status": "stub_completed",
        "computed_at_utc": _utc_now_iso(),
        "module_versions": _module_versions(manifest),
        "artifacts": {
            "manifest_copy": _rel(bundle_paths["manifest_copy"], loaded.repo_root),
            "resolved_manifest": _rel(bundle_paths["resolved_manifest"], loaded.repo_root),
            "registry_record": _rel(bundle_paths["registry_record"], loaded.repo_root),
            "report_ref": _rel(bundle_paths["report_path"], loaded.repo_root),
        },
        "summary": {
            "kind": "stub",
            "items": [
                {
                    "name": "templates_count",
                    "value": len(manifest.get("templates", [])),
                    "kind": "integer",
                    "units": None,
                    "notes": "Count of requested templates.",
                },
                {
                    "name": "invariants_count",
                    "value": len(manifest.get("invariants", [])),
                    "kind": "integer",
                    "units": None,
                    "notes": "Count of requested invariants.",
                },
                {
                    "name": "interface_enabled",
                    "value": bool(manifest.get("interface", {}).get("enabled", False)),
                    "kind": "boolean",
                    "units": None,
                    "notes": "Interface emulator enabled flag.",
                },
                {
                    "name": "redescription_orbit_size",
                    "value": manifest.get("redescription", {}).get("orbit_size"),
                    "kind": "integer",
                    "units": None,
                    "notes": "Requested redescription orbit size.",
                },
            ],
        },
    }


def build_registry_record(loaded: LoadedExperiment, bundle_paths: dict[str, Path]) -> dict[str, Any]:
    manifest = loaded.manifest
    return {
        "record_version": "1.0",
        "experiment_id": manifest["experiment_id"],
        "title": manifest.get("title", manifest["experiment_id"]),
        "experiment_class": manifest["experiment_class"],
        "schema_version": manifest.get("schema_version"),
        "schema_path": _rel(loaded.schema_path, loaded.repo_root),
        "manifest_path": _rel(loaded.manifest_path, loaded.repo_root),
        "manifest_sha256": _manifest_hash(loaded.manifest_path),
        "created_at_utc": _utc_now_iso(),
        "modules": {
            "motif": manifest.get("motif"),
            "field_family": manifest.get("field_family"),
            "kernel_rule": manifest.get("kernel_rule"),
            "templates": manifest.get("templates"),
            "invariants": manifest.get("invariants"),
            "redescription": manifest.get("redescription"),
            "interface": manifest.get("interface", {"enabled": False}),
        },
        "status": "stub_completed",
        "notes": [
            "This record was produced by the standard bundle stub runner.",
            "No scalar-field construction or invariant computation has been executed yet.",
        ],
        "bundle": {
            "manifest_copy": _rel(bundle_paths["manifest_copy"], loaded.repo_root),
            "resolved_manifest": _rel(bundle_paths["resolved_manifest"], loaded.repo_root),
            "registry_record": _rel(bundle_paths["registry_record"], loaded.repo_root),
            "module_versions": _rel(bundle_paths["module_versions"], loaded.repo_root),
            "summary_json": _rel(bundle_paths["summary_json"], loaded.repo_root),
            "summary_csv": _rel(bundle_paths["summary_csv"], loaded.repo_root),
            "artifact_index": _rel(bundle_paths["artifact_index"], loaded.repo_root),
            "report_ref": _rel(bundle_paths["report_path"], loaded.repo_root),
        },
    }


def build_artifact_index(loaded: LoadedExperiment, bundle_paths: dict[str, Path]) -> dict[str, Any]:
    items = []
    for kind, path, role, media_type in [
        ("manifest_copy", bundle_paths["manifest_copy"], "experiment_definition", "application/yaml"),
        ("resolved_manifest", bundle_paths["resolved_manifest"], "resolved_definition", "application/json"),
        ("registry_record", bundle_paths["registry_record"], "run_record", "application/json"),
        ("module_versions", bundle_paths["module_versions"], "module_versions", "application/json"),
        ("summary_json", bundle_paths["summary_json"], "result_summary", "application/json"),
        ("summary_csv", bundle_paths["summary_csv"], "result_summary_table", "text/csv"),
        ("report", bundle_paths["report_path"], "human_report", "text/markdown"),
    ]:
        items.append({
            "kind": kind,
            "path": _rel(path, loaded.repo_root),
            "role": role,
            "sha256": _sha256_bytes(path.read_bytes()),
            "media_type": media_type,
        })
    return {
        "index_version": "1.0",
        "experiment_id": loaded.manifest["experiment_id"],
        "created_at_utc": _utc_now_iso(),
        "artifacts": items,
    }


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2), encoding="utf-8")


def _write_csv_summary(path: Path, summary_payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=["name", "value", "kind", "units", "notes"])
        writer.writeheader()
        for item in summary_payload["summary"]["items"]:
            writer.writerow(item)


def _write_report(path: Path, loaded: LoadedExperiment, summary_payload: dict[str, Any]) -> None:
    manifest = loaded.manifest
    lines = [
        f"# {manifest.get('title', manifest['experiment_id'])}",
        "",
        "## Standard Output Bundle Run",
        "",
        f"- experiment_id: `{manifest['experiment_id']}`",
        f"- experiment_class: `{manifest['experiment_class']}`",
        "- status: `stub_completed`",
        "",
        "## Summary",
        "",
    ]
    for item in summary_payload["summary"]["items"]:
        lines.append(f"- {item['name']}: `{item['value']}`")
    lines += [
        "",
        "## Notes",
        "",
        "- This report was produced by the standard bundle stub runner.",
        "- No scalar-field construction or invariant computation has been executed yet.",
    ]
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines), encoding="utf-8")


def _validate_output(repo_root: Path, payload: dict[str, Any], schema_filename: str, source_name: str) -> None:
    schema = _load_output_schema(repo_root, schema_filename)
    validate_document(payload, schema, source_name=source_name)


def _validate_output_file(repo_root: Path, output_path: Path, schema_filename: str) -> None:
    schema_path = repo_root / "schemas" / schema_filename
    validate_file(output_path, schema_path)


def run_manifest(manifest_path: str | Path, validate: bool = True, repo_root: str | Path | None = None) -> dict[str, str]:
    loaded = load_experiment(manifest_path, validate=validate)
    if repo_root is not None:
        loaded = LoadedExperiment(
            repo_root=Path(repo_root).resolve(),
            manifest_path=loaded.manifest_path,
            manifest=loaded.manifest,
            schema_path=loaded.schema_path,
        )

    manifest = loaded.manifest
    paths = _default_paths(loaded, manifest["experiment_id"])
    paths["experiment_dir"].mkdir(parents=True, exist_ok=True)
    paths["results_dir"].mkdir(parents=True, exist_ok=True)
    paths["artifacts_dir"].mkdir(parents=True, exist_ok=True)
    paths["report_path"].parent.mkdir(parents=True, exist_ok=True)

    timestamp = _timestamp()
    manifest_copy = paths["experiment_dir"] / f"manifest_{timestamp}{loaded.manifest_path.suffix}"
    resolved_manifest_path = paths["experiment_dir"] / "resolved_manifest.json"
    registry_record_path = paths["experiment_dir"] / f"run_{timestamp}.json"
    module_versions_path = paths["results_dir"] / "module_versions.json"
    summary_json_path = paths["results_dir"] / "summary.json"
    summary_csv_path = paths["results_dir"] / "summary.csv"
    artifact_index_path = paths["artifacts_dir"] / "artifact_index.json"
    report_path = paths["report_path"]

    bundle_paths = {
        "manifest_copy": manifest_copy,
        "resolved_manifest": resolved_manifest_path,
        "registry_record": registry_record_path,
        "module_versions": module_versions_path,
        "summary_json": summary_json_path,
        "summary_csv": summary_csv_path,
        "artifact_index": artifact_index_path,
        "report_path": report_path,
    }

    manifest_copy.write_text(loaded.manifest_path.read_text(encoding="utf-8"), encoding="utf-8")

    resolved_manifest = build_resolved_manifest(loaded)
    _validate_output(loaded.repo_root, resolved_manifest, "resolved_manifest.schema.json", str(resolved_manifest_path))
    _write_json(resolved_manifest_path, resolved_manifest)
    _validate_output_file(loaded.repo_root, resolved_manifest_path, "resolved_manifest.schema.json")

    module_versions = _module_versions(manifest)
    _write_json(module_versions_path, module_versions)

    summary_payload = build_result_summary(loaded, bundle_paths)
    _validate_output(loaded.repo_root, summary_payload, "result_summary.schema.json", str(summary_json_path))
    _write_json(summary_json_path, summary_payload)
    _validate_output_file(loaded.repo_root, summary_json_path, "result_summary.schema.json")
    _write_csv_summary(summary_csv_path, summary_payload)

    _write_report(report_path, loaded, summary_payload)

    registry_record = build_registry_record(loaded, bundle_paths)
    _validate_output(loaded.repo_root, registry_record, "registry_record.schema.json", str(registry_record_path))
    _write_json(registry_record_path, registry_record)
    _validate_output_file(loaded.repo_root, registry_record_path, "registry_record.schema.json")

    artifact_index = build_artifact_index(loaded, bundle_paths)
    _validate_output(loaded.repo_root, artifact_index, "artifact_index.schema.json", str(artifact_index_path))
    _write_json(artifact_index_path, artifact_index)
    _validate_output_file(loaded.repo_root, artifact_index_path, "artifact_index.schema.json")

    return {
        "manifest_copy_path": str(manifest_copy),
        "resolved_manifest_path": str(resolved_manifest_path),
        "registry_record_path": str(registry_record_path),
        "module_versions_path": str(module_versions_path),
        "summary_json_path": str(summary_json_path),
        "summary_csv_path": str(summary_csv_path),
        "artifact_index_path": str(artifact_index_path),
        "report_path": str(report_path),
    }


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Read an experiment manifest and write the standard per-suite output bundle.")
    parser.add_argument("manifest", help="Path to the experiment manifest")
    parser.add_argument("--no-validate", action="store_true", help="Skip JSON schema validation")
    parser.add_argument("--repo-root", default=None, help="Optional repository root override")
    args = parser.parse_args()

    result = run_manifest(args.manifest, validate=not args.no_validate, repo_root=args.repo_root)
    print(json.dumps(result, indent=2))
