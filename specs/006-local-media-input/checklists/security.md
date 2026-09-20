# Security Checklist: Local Audio Input

**Purpose**: Review whether local-audio security, privacy, ownership, and failure requirements are complete and unambiguous.
**Created**: 2026-09-21
**Feature**: [Local Audio Input](../spec.md)

**Note**: This custom checklist is a reviewer-owned requirements-quality artifact. It evaluates whether the requirements are written clearly and completely, not whether implementation is complete.
**Review Ownership**: Mark an item `[x]` only when the reviewer determines the requirements-quality criterion is satisfied.
**Marker Semantics**: `[x]` means requirements review passed; it does not mean the implementation is verified.

## Scope and threat model

- [x] CHK001 Does the spec explicitly define the local-only threat boundary, including loopback binding, no public tunnel, no hosted processing, and no telemetry? [Completeness, Spec §6, §10]
- [x] CHK002 Does the spec clearly distinguish user-owned original audio, framework-owned upload/cache copies, app-owned YouTube temporary audio, and generated transcripts? [Clarity, Spec §6]
- [x] CHK003 Does the spec explicitly exclude local video, batch/folder input, cloud upload, and source-file mutation so the security boundary cannot expand silently? [Scope, Spec §2]

## Input and dispatch safety

- [x] CHK004 Are the neither/both/exactly-one input states specified with the required no-backend behavior? [Coverage, Spec §4]
- [x] CHK005 Are supported suffixes enumerated and local video suffixes explicitly rejected before inference? [Completeness, Spec §5, §10]
- [x] CHK006 Does the spec identify the canonical validation boundary so GUI code cannot introduce weaker duplicate validation? [Consistency, Spec §5]
- [x] CHK007 Does the spec require that local input selection cannot invoke yt-dlp or the YouTube cleanup path? [Traceability, Spec §3, §6]

## File and output privacy

- [x] CHK008 Does the spec state that the original local file must remain present and byte-identical after success, failure, cleanup, restart, and cancellation? [Recovery, Spec §3, §6, §10]
- [x] CHK009 Does the spec prohibit deleting, moving, renaming, truncating, or overwriting the original local file? [Completeness, Spec §3]
- [x] CHK010 Are transcript output roots, collision behavior, UTF-8 validation, and controlled download exposure specified without allowing broad file serving? [Clarity, Spec §6, §9]
- [x] CHK011 Does the spec explicitly reject ambient `GRADIO_ALLOWED_PATHS` and broad `allowed_paths` configuration? [Security, Spec §6, §10]

## Error and information disclosure

- [x] CHK012 Are input, dependency, model, inference, and output error categories defined for local-audio failures? [Completeness, Spec §7]
- [x] CHK013 Does the spec require unexpected errors to be sanitized so browser-visible output cannot reveal local paths, cookies, credentials, or tracebacks? [Security, Spec §7, §10]
- [x] CHK014 Does the spec distinguish expected user input errors from sanitized unexpected exceptions without requiring sensitive diagnostic details in the browser? [Clarity, Spec §7]

## Verification and handoff

- [x] CHK015 Does the spec require deterministic tests for dispatch, ownership, privacy, and existing YouTube regression behavior, plus a real local-only Apple Silicon smoke with non-sensitive evidence? [Acceptance, Spec §10, §11]

## Notes

- Mark items `[x]` only after the agent reviewer confirms the requirement-quality criterion is satisfied.
- `$speckit-implement` reads checklist state as a gate and must not modify markers.
- No checklist item authorizes source upload, credentials, OS permissions, or a new release.
