# Chat Handoff for the EAS Scalar-Field Testbed

## Purpose of this note

This note is intended to let any new chat understand what the project is, what is implemented, what is not yet implemented, and how the project is to be used for testing.

This note should travel with any project snapshot uploaded to the File Library.

## What this project is

The EAS Scalar-Field Testbed is a modular research framework for:

1. constructing explicit ordered scalar-field families,
2. varying motifs and kernel rules independently,
3. extracting candidate kernel invariants,
4. testing invariance under admissible redescription,
5. and only then evaluating which interface artifacts are forced.

The project is not primarily a fitting framework. It is a kernel-structure and invariant-discovery framework.

## Governing research rule

The project must be used under this rule:

- Fitted quantities may be used for exploratory guidance.
- Fitted quantities must **not** be treated as evidence for kernel invariants.
- Interface observables must **not** be treated as kernel primitives.

The actual goal is:

> Identify EAS scalar-field invariants that determine the parameters of a kernel mass functional.

## Current project status

The project is **operational as a framework scaffold**, but **not yet complete as a scientific engine**.

### Already implemented

- repository structure
- project standard: `standards/ESTS-1.0.md`
- core schemas in `schemas/`
- example experiment manifest(s) in `experiments/`
- schema validator
- experiment loader
- CLI entry point
- stub runner
- standard per-suite output bundle
- bundle schemas
- schema validation tests for the output bundle
- fail-hard behavior if generated bundle files are invalid

### Not yet implemented in a substantive scientific sense

- real motif engine in `src/motifs/`
- real scalar-field constructor in `src/fields/`
- real kernel-rule engine in `src/kernel_rules/`
- real canonical template extractor in `src/templates/`
- real invariant engine in `src/invariants/`
- real redescription engine in `src/redescriptions/`
- real interface emulator in `src/interface/`

So the current project can manage and validate experiments correctly, but it does not yet compute full scientific EAS results except where specific exploratory code has been added later.

## How the project is organized

The project standard assumes seven modules:

- motif generator
- explicit scalar-field constructor
- kernel rule engine
- canonical template extractor
- invariant engine
- admissible redescription engine
- interface emulator

The first mandatory experiment family is **motif variation**.

## What a new chat should use this repository for

A new chat should use this repository to:

1. read the project standard,
2. inspect the schemas,
3. inspect manifests,
4. validate manifests and output bundles,
5. add or edit modules in `src/`,
6. add experiment manifests,
7. extend the registry/output contract,
8. run and interpret testbed experiments while respecting the governing rule that fitted results are not evidence for kernel ontology.

## What a new chat should not assume

A new chat should **not** assume that:

- previously explored motifs are correct,
- previously explored muon/electron/tau constructions are validated physical motifs,
- fitted functionals identify true invariants,
- interface readouts define kernel structure.

In particular, many earlier exploratory runs were useful only as scaffolding and rejection tests.

## Current methodological position

The present methodological position is:

1. Motif choice may be wrong.
2. Scalar-field rule choice may be wrong.
3. Candidate invariant choice may be wrong.
4. Interface emulation choice may be wrong.

Therefore the testbed must always preserve modular blame assignment.

A failure must be attributable to one of:

- motif,
- field construction,
- kernel rule,
- invariant definition,
- interface readout.

## Standard per-suite output bundle

Every test suite should produce a standard bundle under `registry/`:

- experiment manifest copy
- resolved manifest
- registry record
- module versions file
- summary JSON
- summary CSV
- artifact index
- human-readable report

These are part of the project standard and should be preserved in any serious run.

## How a new chat should use the project for testing

When asked to use the repository for testing, a new chat should proceed in this order:

1. Read `README.md`.
2. Read `standards/ESTS-1.0.md`.
3. Read this handoff note.
4. Inspect `schemas/` and `experiments/`.
5. Determine whether the task is:
   - schema/manifest work,
   - framework/runner work,
   - motif work,
   - scalar-field construction work,
   - invariant work,
   - redescription work,
   - interface-emulation work.
6. Use or extend the appropriate module(s) under `src/`.
7. Preserve the per-suite output bundle under `registry/`.
8. State clearly whether the result is:
   - exploratory,
   - heuristic,
   - evidential.

## Classification rule for results

Every result should be treated as one of:

### Exploratory
Used for search and intuition only.

### Heuristic
Useful for narrowing constructions, but not evidential.

### Evidential
May support a kernel-side claim only if:

- the motif is explicit,
- the scalar-field construction is explicit,
- the invariant is non-fitted,
- redescription stability is tested,
- provenance is complete.

## Immediate next priority if no other instruction is given

If a new chat is given the repository with no additional instruction, the default next priority is:

> implement one real end-to-end experiment path through motifs, fields, templates, invariants, and redescription testing, without relying on fitted quantities as kernel evidence.

A good first full path is:

1. one real motif object,
2. one real explicit scalar-field constructor,
3. one real outer template,
4. one real core template,
5. one real invariant calculation,
6. one real redescription test.

## Practical instruction for any new chat

Treat this repository as a **testing instrument**, not as a completed theory.

Use it to:

- formalize candidate constructions,
- run controlled experiments,
- reject unstable or non-invariant quantities,
- and preserve all results with provenance.

Do not treat a successful fit as proof of kernel truth.

## Files a new chat should read first

1. `README.md`
2. `standards/ESTS-1.0.md`
3. `docs/chat_handoff.md`
4. relevant files in `schemas/`
5. relevant manifests in `experiments/`
6. relevant runtime files in `src/common/`

## Short summary

The project is ready to be used as a disciplined manifest-driven testbed scaffold.
It is not yet a complete scientific engine.
Its primary scientific purpose is invariant discovery in explicit EAS scalar-field constructions, under strict separation of kernel structure from interface readout.
