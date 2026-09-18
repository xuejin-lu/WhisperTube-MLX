# UX & Accessibility Requirements Checklist: Local Graphical UI

**Purpose**: Review primary flow, state, recovery, preview/download, and accessibility requirement quality.
**Created**: 2026-09-19
**Feature**: [spec.md](../spec.md)

**Review Ownership**: Reviewer-owned requirements-quality artifact; `[x]` means the criterion was reviewed
and satisfied, not that implementation is complete.

## Primary Flow

- [x] CHK001 Are the URL input, single Transcribe action, and non-Terminal task outcome explicitly defined? [Completeness, Spec §US1, FR-001]
- [x] CHK002 Is blank-input behavior unambiguous and separated from pipeline URL validation? [Clarity, Spec §US1/AC2, FR-003]
- [x] CHK003 Is one-active-run behavior specified for pending and running interactions? [Coverage, Spec §US1/AC3, FR-004]

## State and Recovery

- [x] CHK004 Are idle, running, success, and error states all defined with objective transitions? [Completeness, Spec §FR-004, SC-002]
- [x] CHK005 Are stale preview/download clearing and action restoration defined for retry after success or failure? [Recovery, Spec §FR-004, FR-007]
- [x] CHK006 Are cause-specific and unexpected errors presented with distinct, actionable, non-technical outcomes? [Consistency, Spec §US2, FR-008]

## Transcript Result

- [x] CHK007 Are preview completeness and download byte-equivalence measurable? [Measurability, Spec §FR-005, SC-003]
- [x] CHK008 Are missing, empty, unreadable, invalid-encoding, wrong-type, and disallowed-path results covered? [Edge Cases, Spec §US3/AC2, SC-004]

## Accessibility and Scope

- [x] CHK009 Are visible labels and normal keyboard navigation requirements defined for every interactive/status surface? [Coverage, Spec §FR-014]
- [x] CHK010 Are packaging, multiple jobs/users, model selection controls, and advanced transcript features clearly excluded or deferred? [Scope, Assumptions]

## Notes

- Leave unchecked until the pre-implementation Agent Reviewer Phase.
- `$speckit-implement` treats markers as read-only.
