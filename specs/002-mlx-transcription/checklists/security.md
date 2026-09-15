# Security Requirements Checklist: Local MLX Transcription

**Purpose**: Review privacy, local-data handling, and failure-boundary requirements before implementation.
**Created**: 2026-09-16
**Feature**: [spec.md](../spec.md)
**Review Ownership**: Agent reviewer phase, per `docs/CHECKLIST_REVIEW_POLICY.md`.

## Privacy and Local Processing

- [x] Are local-only handling requirements defined for audio, model caches, transcripts, and telemetry? [Spec §FR-002, FR-009]
- [x] Is the boundary between model retrieval and prohibited hosted transcription explicit? [Spec §FR-002, Assumptions]
- [x] Is the no-credentials/no-upload requirement objectively assessable? [Spec §FR-009, SC-004]

## Input and Output Safety

- [x] Are missing, non-file, unreadable, and unsupported inputs distinguished? [Spec §FR-006, Edge Cases]
- [x] Are unsafe, unwritable, and colliding output paths covered without silent overwrite? [Spec §FR-008, Edge Cases]
- [x] Are audio and model artifacts prevented from entering versioned paths? [Spec §FR-009, Key Entities]

## Failure and Verification Boundaries

- [x] Are dependency, model, load, inference, and output failures separately actionable? [Spec §FR-007–FR-008]
- [x] Is the Apple Silicon/hardware-dependent smoke boundary separated from deterministic CI? [Spec §SC-002, SC-004]
- [x] Are claims limited when no labeled accuracy corpus exists? [Spec §SC-005, Assumptions]

## Notes

- Newly generated items remain unchecked until the pre-implementation reviewer confirms them.
