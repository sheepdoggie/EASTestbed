# EAS Scalar-Field Testbed

This repository is a standards-based, schema-backed, manifest-driven framework for EAS scalar-field investigations.

## Purpose

The testbed exists to let motif choice, scalar-field construction, kernel rules, template extraction, invariant computation, admissible redescription, and interface emulation vary independently.

The goal is to identify non-fitted EAS scalar-field invariants that may parameterize a kernel mass functional.

## Seven modules

The project standard organizes the testbed into seven modules:

1. **Motif Generator** (`M`)
2. **Explicit Scalar-Field Constructor** (`F`)
3. **Kernel Rule Engine** (`K`)
4. **Canonical Template Extractor** (`T`)
5. **Invariant Engine** (`I`)
6. **Admissible Redescription Engine** (`R`)
7. **Interface Emulator** (`O`)

An experiment is therefore a structured object of the form

```text
E = (M, F, K, T, I, R, O)
```

## How the schemas relate to the modules

### `schemas/motif.schema.json`
Defines the output of the **Motif Generator**.
It specifies motif identity, plateau regions, structural relations, sign metadata, provenance, and motif-family variation metadata.

### `schemas/field_family.schema.json`
Defines the output of the **Explicit Scalar-Field Constructor**.
It specifies ordered scalar families, layer counts, closure-cell support, shell structure, dressing structure, neutral-excess sectors, and reconciliation-band metadata.

### `schemas/template.schema.json`
Defines the output of the **Canonical Template Extractor**.
It specifies support regions, local extraction rules, residual-plane projections, normalization conventions, and template provenance.

### `schemas/invariant.schema.json`
Defines the output of the **Invariant Engine**.
It specifies candidate invariant values, redescription-stability results, class-separation diagnostics, admissibility status, and interpretation metadata.

### `schemas/experiment.schema.json`
Defines the **experiment manifest** itself.
It binds together module references, experiment class, run configuration, overrides, outputs, and provenance.

## How manifests drive experiments

Each experiment manifest should:

- identify the experiment class,
- reference a motif specification,
- reference a scalar-field constructor,
- reference kernel rules,
- list canonical templates,
- list candidate invariants,
- define the redescription orbit generator,
- optionally define the interface emulator,
- define outputs and provenance.

The code should read a manifest, resolve the required module objects, execute them in order, and write a complete experiment record.

## First mandatory experiment family

The first mandatory experiment family is **motif variation**.

That means the testbed must be able to vary motifs while keeping the scalar-field constructor, kernel rules, invariant definitions, and interface emulator fixed.

## Repository landmarks

- `standards/ESTS-1.0.md` — governing project standard
- `schemas/` — machine-readable schemas
- `experiments/` — manifest-driven experiments
- `src/` — reusable implementation modules
- `registry/` — experiment records and results

## Minimal workflow

1. Define or select a motif.
2. Construct an explicit ordered scalar family.
3. Apply kernel rules.
4. Extract canonical templates.
5. Compute candidate invariants.
6. Test redescription stability.
7. Optionally emulate interface artifacts.
8. Store the complete experiment record.
