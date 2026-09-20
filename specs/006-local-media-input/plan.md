# Implementation Plan: Local Audio Input

**Branch**: `006-local-media-input` | **Date**: 2026-09-21 | **Spec**: `specs/006-local-media-input/spec.md`

## Summary

Add a second, mutually exclusive local-audio route to the existing Gradio GUI. The GUI will dispatch a YouTube URL to the approved `run_pipeline()` path or a selected local audio path directly to the existing `transcribe_audio()` boundary. Existing transcript validation, preview/download handling, loopback-only launch settings, error categories, and YouTube cleanup remain shared and unchanged.

## Technical Context

**Language/Version**: Python 3.13 development runtime; supported native Apple Silicon Python 3.10+ release path

**Primary Dependencies**: Gradio 6.27.0, MLX Whisper, OpenCC, existing `whispertube.pipeline` and `whispertube.transcription` modules

**Storage**: User-selected local audio is read-only input; framework upload/cache copies and generated transcripts remain in ignored local runtime paths

**Testing**: Python `unittest`, existing Gradio configuration/privacy tests, mocked transcription/pipeline boundaries, and one real Apple Silicon local-audio GUI smoke

**Target Platform**: macOS 14+ on Apple Silicon; loopback-only local browser GUI

**Project Type**: Local desktop GUI plus Python CLI/library modules

**Performance Goals**: No new latency target; local audio follows the existing MLX transcription runtime and one-active-job GUI queue

**Constraints**: No hosted upload, public tunnel, telemetry, broad `allowed_paths`, source-file mutation, duplicate Whisper stack, or new release/tag during implementation

**Scale/Scope**: One URL or one supported local audio file per request; seven approved audio suffixes; no batch/folder/video input

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- **Local-First Processing**: PASS. Local files are transcribed through the existing local MLX boundary.
- **Privacy-First Handling**: PASS. The original source is read-only, no external service is added, and only validated Markdown is exposed for download.
- **Spec-Driven Development**: PASS. This plan, the existing feature spec, contract, generated checklist, and tasks will remain aligned.
- **Test-First Quality**: PASS. Dispatch, validation, ownership, privacy, and regression tests precede implementation changes.
- **Reliability and Small Slices**: PASS. The first slice adds dispatch/ownership behavior while reusing existing pipeline and transcription code.

## Design Decisions

### Input dispatch

`build_app()` adds one `gr.File` input configured for a single filepath and the seven approved audio suffixes. The terminal handler accepts both URL and local-file values and applies the contract before calling a backend:

- URL only: call `run_pipeline()` exactly once.
- Local file only: call `transcribe_audio()` exactly once.
- Neither or both: return a safe input error without calling either backend.

The local handler passes the Gradio-managed filepath to `transcribe_audio()` and does not add a new media-processing abstraction. `transcribe_audio()` remains the canonical suffix/readability/output-collision validation boundary.

### Ownership and cleanup

The local route never calls the YouTube pipeline cleanup path and never deletes, moves, renames, truncates, or overwrites the selected source. A framework-owned upload/cache copy may be cleaned by Gradio's existing cache policy. Output collision behavior remains the existing clear `OutputError` rather than silent overwrite.

### GUI safety

The existing `load_transcript_result()` path continues to validate transcript root, suffix, readability, non-empty content, preview bytes, and download exposure. Existing loopback-only launch configuration, private events, strict CORS, disabled analytics/monitoring, one-active-job behavior, and ambient `GRADIO_ALLOWED_PATHS` rejection remain unchanged.

### Error mapping

The GUI will preserve the existing categories for `PipelineError` and `TranscriptionError`. Expected local input errors remain input errors; unexpected exceptions remain the generic sanitized application error and must not expose a local path, traceback, cookie, or credential.

## Project Structure

### Documentation (this feature)

```text
specs/006-local-media-input/
├── spec.md
├── plan.md
├── research.md
├── data-model.md
├── quickstart.md
├── contracts/ui.md
├── checklists/security.md
└── tasks.md
```

### Source and tests

```text
whispertube/
├── gui.py                 # dispatch, Gradio File input, safe result/error handling
└── transcription.py       # existing canonical local-audio validation/inference boundary

tests/
├── test_gui.py            # dispatch, UI contract, ownership/privacy/error tests
└── test_transcription.py  # existing suffix, collision, and write-boundary regression suite

README.md                  # user-facing URL-or-local-audio workflow and suffix documentation
docs/STATUS.md             # review evidence and current feature state
```

**Structure Decision**: Keep the existing single-project Python layout. Local-audio selection is a GUI dispatch extension, not a new service or duplicate transcription implementation.

## Test Strategy

1. RED: add the smallest tests for mutually exclusive dispatch and local-only transcription before changing `gui.py`.
2. GREEN: implement the shared request dispatcher and one `gr.File` input using existing backends.
3. RED/GREEN: add ownership, suffix, output-collision, privacy, and UI regression tests; make only the minimum changes required.
4. REFACTOR: simplify duplicated handler/state wiring while focused and full suites remain green.
5. Run the full deterministic suite, then a real local GUI smoke using a non-sensitive untracked supported audio fixture and `mlx-community/whisper-tiny`.

## Implementation Phases

1. **Foundation**: generate and review the requirements/security checklists, tasks, and cross-artifact analysis.
2. **US1 dispatch**: add deterministic URL/local-file dispatch and local transcription integration tests, then implement the route.
3. **US2 ownership and errors**: prove source byte preservation across success/inference failure/output failure and sanitize unexpected errors.
4. **US3 regression and UX**: preserve YouTube behavior/privacy configuration, update README, and run GUI smoke.
5. **Polish/convergence**: run full tests, artifact inspection, converge, update status, push, and verify exact-HEAD CI.

## Complexity Tracking

No constitution violations or complexity exceptions are required. The design reuses the existing transcription and GUI result-validation boundaries.
