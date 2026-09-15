# Implementation Plan: Local MLX Transcription

**Branch**: `002-mlx-transcription` | **Date**: 2026-09-16 | **Spec**: [spec.md](spec.md)

**Input**: Feature specification from `/specs/002-mlx-transcription/spec.md`

**Note**: This template is filled in by the `$speckit-plan` command; its definition describes the execution workflow.

## Summary

Add a local transcription boundary for one audio file. The CLI validates local paths, lazily loads
the selected MLX Whisper backend, requests Chinese transcription, converts returned text to Taiwan
Traditional Chinese locally, groups it into readable paragraphs, and writes one Markdown artifact
beneath an ignored runtime directory.
Keep the v0.1 YouTube downloader separate until v0.3 composition.

## Technical Context

<!--
  ACTION REQUIRED: Replace the content in this section with the technical details
  for the project. The structure here is presented in advisory capacity to guide
  the iteration process.
-->

**Language/Version**: Python 3.10+ (development target Python 3.11+)

**Primary Dependencies**: `mlx-whisper` 0.4.3 API, Apple MLX runtime, `ffmpeg`, OpenCC Python API;
dependencies are installed only for local macOS inference, while deterministic CI uses fakes.

**Storage**: Ignored local files under `temp/transcripts/`; MLX model cache remains local and ignored.

**Testing**: Python `unittest` for deterministic unit/contract tests; local Apple Silicon integration
and smoke tests for real MLX inference; CI excludes model downloads and hardware-only work.

**Target Platform**: macOS on Apple Silicon (M1/M2/M3/M4 family)

**Project Type**: Python CLI and reusable local library module

**Performance Goals**: A short fixture completes in a local smoke run without imposing a fixed
wall-clock SLA; the selected model and elapsed time are recorded for review.

**Constraints**: Local-first/privacy-first; no hosted inference or telemetry; one input and one
Markdown output; default large-v3 target with explicit smaller-model override; repository-relative
runtime output remains under ignored roots, with explicit system-temporary paths allowed; no silent
overwrite; input/output/model failures remain cause-specific; v0.1 downloader is not modified.

**Scale/Scope**: One local maintainer, one audio file per invocation, one transcript artifact; no
GUI, batch orchestration, summarization, diarization, word timestamps, or YouTube composition.

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- PASS — inference and text conversion remain local; no hosted transcription dependency is added.
- PASS — audio, model caches, and transcripts are written only to ignored local paths.
- PASS — the spec defines measurable acceptance and the plan keeps deterministic tests independent
  from MLX hardware/network/model downloads.
- PASS — dependency and model errors are separated from input, output, and inference failures.
- PASS — the change is a small vertical slice and does not alter the proven v0.1 downloader.

## Project Structure

### Documentation (this feature)

```text
specs/002-mlx-transcription/
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
├── youtube.py              # existing v0.1 acquisition boundary, unchanged
└── transcription.py        # v0.2 validation, MLX adapter, formatting, and CLI

tests/
├── test_youtube.py         # existing v0.1 tests
└── test_transcription.py   # deterministic v0.2 tests

requirements-macos.txt      # local MLX Whisper, MLX runtime, ffmpeg/OpenCC guidance

specs/002-mlx-transcription/
├── spec.md
├── plan.md
├── research.md
├── data-model.md
├── quickstart.md
├── contracts/cli.md
└── tasks.md
```

**Structure Decision**: Keep the existing small Python package and add one isolated transcription
module. Tests inject a fake backend and converter for deterministic coverage; the real MLX adapter
is imported lazily so CI does not require Apple Silicon or model downloads. Runtime artifacts stay
under ignored `temp/` paths.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| None | N/A | The feature fits one package and one local pipeline stage. |
