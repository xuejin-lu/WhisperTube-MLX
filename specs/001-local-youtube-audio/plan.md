# Implementation Plan: Local YouTube Audio Acquisition

**Branch**: `001-local-youtube-audio` | **Date**: 2026-09-16 | **Spec**: [spec.md](spec.md)

**Input**: Feature specification from `/specs/001-local-youtube-audio/spec.md`

**Note**: This template is filled in by the `$speckit-plan` command; its definition describes the execution workflow.

## Summary

Provide a small local CLI for one-video YouTube audio acquisition. Normalize supported URL forms
before invoking the local `yt-dlp` executable, force single-video behavior, write output beneath an
ignored runtime directory, and expose a browser-session fallback without exporting credentials.
Keep URL handling and command construction deterministic and independently testable.

## Technical Context

<!--
  ACTION REQUIRED: Replace the content in this section with the technical details
  for the project. The structure here is presented in advisory capacity to guide
  the iteration process.
-->

**Language/Version**: Python 3.10+ (standard library; development target Python 3.11+)

**Primary Dependencies**: `yt-dlp` executable supplied by the local environment; no Python runtime
dependency for the core module

**Storage**: Local ignored runtime files under `temp/audio/`; no persistent application database

**Testing**: Python `unittest` for deterministic unit tests; local smoke test for real acquisition

**Target Platform**: macOS on Apple Silicon (M1/M2/M3/M4 family)

**Project Type**: Python CLI and small reusable library module

**Performance Goals**: Start one acquisition promptly after validation; downloader performance is
determined by the source and local network, not by an application SLA in v0.1

**Constraints**: Local-first and privacy-first; no playlist batch mode; no cookie export; relative
runtime artifacts stay under ignored `temp/` or `outputs/` paths; absolute system-temp paths are
allowed; unwritable output paths fail before downloader start; deterministic tests must not require
YouTube, browser credentials, private media, or Apple Silicon acceleration

**Scale/Scope**: One requested video per CLI invocation, one local maintainer, one ignored output
directory; transcription and GUI are later milestones

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- PASS — local processing is preserved; no hosted download, tunnel, or cloud transcription is added.
- PASS — media and browser credentials remain local and are never exported or committed.
- PASS — the feature has an acceptance-oriented spec and will retain deterministic tests.
- PASS — the implementation is a small vertical slice with no speculative abstraction or GUI.
- PASS — live YouTube behavior is separated from deterministic CI tests and reported truthfully.

## Project Structure

### Documentation (this feature)

```text
specs/[###-feature]/
├── plan.md              # This file ($speckit-plan command output)
├── research.md          # Phase 0 output ($speckit-plan command)
├── data-model.md        # Phase 1 output ($speckit-plan command)
├── quickstart.md        # Phase 1 output ($speckit-plan command)
├── contracts/           # Phase 1 output ($speckit-plan command)
└── tasks.md             # Phase 2 output ($speckit-tasks command - NOT created by $speckit-plan)
```

### Source Code (repository root)
<!--
  ACTION REQUIRED: Replace the placeholder tree below with the concrete layout
  for this feature. Delete unused options and expand the chosen structure with
  real paths (e.g., apps/admin, packages/something). The delivered plan must
  not include Option labels.
-->

```text
whispertube/
├── __init__.py
└── youtube.py              # URL normalization, command construction, and CLI

tests/
└── test_youtube.py         # deterministic unit tests

specs/001-local-youtube-audio/
├── spec.md
├── plan.md
├── research.md
├── data-model.md
├── quickstart.md
├── contracts/cli.md
└── tasks.md
```

**Structure Decision**: Keep the existing small Python package and test directory. The CLI remains
in the feature module so URL parsing and command construction can be imported directly by tests,
while runtime media is kept outside versioned source under the ignored `temp/` path.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| None | N/A | The feature fits one package and has no complexity violation. |
