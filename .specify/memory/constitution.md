<!--
Sync Impact Report
- Version change: template → 1.0.0
- Modified principles: template placeholders → Local-First Processing, Privacy-First Handling,
  Spec-Driven Development, Test-First Quality, Reliability and Small Slices
- Added sections: Additional Constraints; Development Workflow and Quality Gates
- Removed sections: none
- Follow-up TODOs: none
-->

# WhisperTube-MLX Constitution

## Core Principles

### I. Local-First Processing

YouTube acquisition, audio processing, speech recognition, post-processing, and transcript
generation MUST run locally on the user's Apple Silicon Mac by default. The product MUST NOT
reintroduce hosted download proxies, remote transcription services, public tunnels, or cloud
processing unless the product specification is explicitly amended. This keeps the core workflow
available without paid services and keeps user media under the user's control.

### II. Privacy-First Handling

The project MUST NOT upload media, browser cookies, browser profiles, transcripts, credentials, or
telemetry by default. Cookies and browser sessions MUST be treated as credentials and MUST NOT be
committed or copied into repository-managed output. Downloaded media, private recordings, model
caches, and generated private transcripts MUST remain ignored and local. Any exception requires an
explicitly documented product decision and user-visible behavior.

### III. Spec-Driven Development

Meaningful feature work MUST have a written acceptance-oriented specification before implementation,
with a plan and ordered tasks when the work is more than a tiny fix. The specification, plan, tasks,
tests, and implementation MUST remain mutually consistent. Product scope MUST NOT expand silently;
unresolved product choices MUST be surfaced as decisions rather than guessed in code.

### IV. Test-First Quality

Behavior changes MUST follow the TDD sequence: write the smallest failing test for the next
acceptance criterion, implement the minimum behavior to pass it, then refactor only while the suite
remains green. Pure logic MUST have deterministic unit tests. Integration and hardware-, browser-,
or network-dependent behavior MUST use the narrowest applicable integration or smoke test. A
behavior MUST NOT be reported as verified when its required test was not actually run.

### V. Reliability and Small Slices

Work MUST advance one independently reviewable capability at a time, with the smallest change that
meets the current milestone. Each pipeline stage MUST be validated before dependent UI or workflow
layers are added. The project MUST prefer simple, testable designs over speculative abstractions,
and MUST distinguish download, transcription, and output failures when the end-to-end pipeline is
introduced. This reduces maintenance cost for a single-maintainer project and makes failures
actionable.

## Additional Constraints

- The initial target platform is macOS on Apple Silicon (M1/M2/M3/M4 family). Windows, Linux,
  Intel Mac, hosted GPU deployment, and paid API fallbacks are out of scope for early milestones.
- The primary product path is `YouTube URL → local audio → local MLX Whisper → Taiwan Traditional
  Chinese Markdown transcript`.
- YouTube work MUST process one requested video. Playlist parameters MAY be present in an input URL
  but MUST NOT trigger playlist batch processing during v0.1.
- The repository MUST use free or open-source dependencies for normal operation and MUST NOT add
  telemetry, user accounts, a database, or a hosted service before the core pipeline is stable.
- Downloaded audio and other runtime artifacts MUST be written only to ignored local paths. The
  repository MUST never contain cookies, credentials, private media, model caches, or generated
  private transcripts.

## Development Workflow and Quality Gates

- Codex MUST synchronize the configured Git remote, preserve existing user work, and read the
  current repository instructions before selecting the next task.
- For each behavior-changing task, Codex MUST record RED, GREEN, and applicable REFACTOR evidence;
  run focused tests and the full deterministic suite; and run local integration or smoke tests when
  technically possible.
- Spec Kit artifacts are the source of truth for feature intent. A feature MUST be checked for
  convergence against its specification, plan, tasks, constitution, implementation, and tests
  before it is presented for review.
- Commits MUST be coherent and use a conventional prefix where practical. Completed work MUST be
  pushed to the configured GitHub remote, and deterministic CI MUST be green or explicitly pending
  with no known failure before the work is called review-ready.
- Human involvement MUST be limited to genuine authorization or product decisions, such as browser
  login, Keychain approval, macOS privacy permission, or an unresolved product alternative. Routine
  shell commands, tests, installs, local smoke tests, and Git operations belong to Codex when the
  environment permits them.
- Every development report MUST state the active specification, acceptance criteria addressed,
  TDD evidence, validation results, human gates, convergence status, risks, pushed commit, and one
  exact next action.

## Governance

This constitution is the highest-level project guidance. When another document conflicts with it,
the constitution takes precedence until an amendment is approved. Every feature review MUST check
compliance with the principles and constraints above, including privacy handling and the truthfulness
of verification claims.

Amendments require a documented rationale, an update to the affected Spec Kit artifacts and
workflow guidance, and a review of tests or migration tasks made necessary by the change. The
amendment MUST update the Sync Impact Report and the Last Amended date. Version numbers use semantic
versioning: MAJOR for incompatible principle or governance changes, MINOR for new or materially
expanded principles or sections, and PATCH for clarifications that do not change obligations.

The maintainer owns product direction and approves material governance changes. Codex MUST enforce
the current constitution during implementation and report any conflict or missing decision instead
of silently bypassing it. The constitution is reviewed whenever the product milestone, security
model, target platform, or development workflow changes materially.

**Version**: 1.0.0 | **Ratified**: 2026-09-16 | **Last Amended**: 2026-09-16
