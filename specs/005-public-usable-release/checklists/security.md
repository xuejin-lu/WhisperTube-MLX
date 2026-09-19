# Security & Privacy Requirements Checklist: Public Usable Release

**Purpose**: Review whether v1.0 installation, launch, runtime-artifact, release, and troubleshooting requirements preserve the project's local-first and privacy-first boundaries.
**Created**: 2026-09-19
**Feature**: [spec.md](../spec.md)

**Review Ownership**: This is a reviewer-owned requirements-quality artifact. Mark `[x]` only when the criterion is satisfied by the spec/plan/tasks; `[x]` does not mean implementation is complete.

## Installation and Runtime Trust Boundary

- [x] CHK001 Is the supported host boundary (native Apple Silicon, supported macOS, native Python, and local decoder) explicit and objectively diagnosable? [Completeness, Spec §FR-001, FR-005]
- [x] CHK002 Are setup idempotence and non-destructive behavior specified for existing environments, outputs, caches, cookies, credentials, and unrelated files? [Recovery, Spec §FR-003, Edge Cases]
- [x] CHK003 Does the setup requirement prohibit silent privilege escalation, package-manager installation, and unrelated system mutation? [Least Privilege, Plan §Technical Context, Spec §Assumptions]
- [x] CHK004 Are dependency, model-download, and network-failure boundaries documented without implying that private data is uploaded? [Failure Handling, Spec §FR-005, FR-009, FR-014]

## Local Network and File Exposure

- [x] CHK005 Are loopback-only binding, no public share/tunnel, and no telemetry requirements consistent across the release flow and existing GUI contract? [Consistency, Spec §FR-010, SC-002]
- [x] CHK006 Does the specification explicitly protect browser cookies, profiles, credentials, media, transcripts, and model caches from export or repository/release artifacts? [Coverage, Spec §FR-009, FR-018]
- [x] CHK007 Are runtime audio, transcript, temporary, and model-cache ownership, location, retention, and deletion boundaries defined? [Completeness, Spec §FR-011, FR-012]
- [x] CHK008 Is ambient configuration that could broaden Gradio file serving addressed as a preserved v0.4 privacy boundary? [Configuration Safety, Spec §FR-010, Edge Cases]

## Release Artifact and Documentation Safety

- [x] CHK009 Are release-candidate artifact inspection requirements specific enough to detect credentials, cookies, private media/transcripts, model caches, and accidental absolute machine paths? [Measurability, Spec §FR-018, SC-005]
- [x] CHK010 Does the release plan prohibit automatic GitHub Release publication and distinguish candidate preparation from the final human approval action? [Authorization Boundary, Spec §FR-017, Assumptions]
- [x] CHK011 Are troubleshooting instructions required to preserve cause-specific errors and avoid requesting secrets or copying browser credentials into the checkout? [Credential Handling, Spec §FR-014, User Story 3]
- [x] CHK012 Are browser-cookie fallback and macOS permission/login situations explicitly identified as possible Human Gates rather than automated assumptions? [Human Gate, Spec §FR-014, Assumptions]

## Validation Quality

- [x] CHK013 Are deterministic privacy/configuration tests separated from network, model, browser, and Apple Silicon smoke evidence? [Test Isolation, Spec §FR-015, FR-016]
- [x] CHK014 Does the release candidate require evidence that cleanup does not delete retained transcripts or unrelated pre-existing artifacts? [Recovery, Spec §FR-003, FR-007, SC-003]
- [x] CHK015 Are out-of-scope hosted processing, public tunnels, paid APIs, accounts, databases, telemetry, and additional workflow data explicitly excluded? [Scope, Spec §FR-019, Out of Scope]

## Notes

- Reviewed item-by-item in the pre-implementation Agent Reviewer Phase on 2026-09-19.
- CHK012 was initially identified as underspecified; the spec, plan, and T019 now explicitly state that browser login/cookie, Keychain, and macOS privacy prompts are user-owned gates that must not be bypassed or captured.
- `$speckit-implement` reads checklist state but does not modify markers.
