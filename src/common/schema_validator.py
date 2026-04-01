from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import yaml
from jsonschema import Draft202012Validator


class SchemaValidationError(Exception):
    """Raised when a document fails JSON schema validation."""


def load_document(path: str | Path) -> Any:
    """Load a JSON or YAML document from disk."""
    file_path = Path(path)
    suffix = file_path.suffix.lower()
    with file_path.open("r", encoding="utf-8") as handle:
        if suffix in {".yaml", ".yml"}:
            return yaml.safe_load(handle)
        if suffix == ".json":
            return json.load(handle)
    raise ValueError(f"Unsupported document type for {file_path}")


def load_schema(path: str | Path) -> dict[str, Any]:
    """Load a JSON schema from disk."""
    data = load_document(path)
    if not isinstance(data, dict):
        raise TypeError(f"Schema at {path} must be a JSON object")
    return data


def validate_document(document: Any, schema: dict[str, Any], source_name: str = "<memory>") -> None:
    """Validate a document against a schema.

    Raises:
        SchemaValidationError: if validation fails.
    """
    validator = Draft202012Validator(schema)
    errors = sorted(validator.iter_errors(document), key=lambda err: list(err.path))
    if not errors:
        return

    lines = [f"Schema validation failed for {source_name}:"]
    for err in errors:
        location = "/".join(str(part) for part in err.absolute_path) or "<root>"
        lines.append(f"- {location}: {err.message}")
    raise SchemaValidationError("\n".join(lines))


def validate_file(document_path: str | Path, schema_path: str | Path) -> Any:
    """Load and validate a file against a schema, returning the parsed document."""
    document = load_document(document_path)
    schema = load_schema(schema_path)
    validate_document(document, schema, str(document_path))
    return document


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Validate a JSON/YAML file against a JSON schema.")
    parser.add_argument("document", help="Path to the JSON or YAML document")
    parser.add_argument("schema", help="Path to the JSON schema")
    args = parser.parse_args()

    validate_file(args.document, args.schema)
    print(f"OK: {args.document} is valid against {args.schema}")
