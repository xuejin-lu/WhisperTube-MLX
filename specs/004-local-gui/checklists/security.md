# Security & Privacy Requirements Checklist: Local Graphical UI

**Purpose**: Review local binding, telemetry, file exposure, error, and credential requirement quality.
**Created**: 2026-09-19
**Feature**: [spec.md](../spec.md)

**Review Ownership**: Reviewer-owned requirements-quality artifact; `[x]` means the criterion was reviewed
and satisfied, not that implementation is complete.

## Local Network Boundary

- [x] CHK001 Are loopback-only binding and public share/tunnel prohibition explicit and testable? [Completeness, Spec §FR-009]
- [x] CHK002 Are telemetry, analytics, and monitoring defaults explicitly prohibited rather than left to framework defaults? [Clarity, Spec §FR-009–FR-010]
- [x] CHK003 Are direct API and cross-origin exposure boundaries defined consistently with a single-user local app? [Coverage, Spec §FR-009]

## Local File Boundary

- [x] CHK004 Is transcript preview/download eligibility restricted by root, type, existence, readability, encoding, and non-empty content? [Completeness, Spec §FR-006]
- [x] CHK005 Are arbitrary, pre-existing unrelated, media, cookie, browser-profile, credential, and model paths explicitly protected from GUI exposure? [Coverage, Spec §FR-006, FR-010]
- [x] CHK006 Is stale preview/download clearing specified for both new runs and every failure path? [Recovery, Spec §FR-007]

## Error and Credential Handling

- [x] CHK007 Are approved error categories preserved while traceback and sensitive-data disclosure are prohibited? [Consistency, Spec §FR-008]
- [x] CHK008 Are browser login, cookie fallback, and macOS permission boundaries identified as exceptional Human Gates without exporting credentials? [Coverage, Edge Cases]

## Validation Boundaries

- [x] CHK009 Are deterministic security tests independent of live media, credentials, models, and hardware? [Completeness, Spec §FR-012]
- [x] CHK010 Does the real smoke requirement record local binding, cleanup, retention, and Human Gate outcomes without storing private contents? [Measurability, Spec §FR-013, SC-007]

## Notes

- Leave unchecked until the pre-implementation Agent Reviewer Phase.
- `$speckit-implement` treats markers as read-only.
