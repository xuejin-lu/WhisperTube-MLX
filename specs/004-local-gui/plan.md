# Implementation Plan: Local Graphical UI

**Branch**: `004-local-gui` | **Date**: 2026-09-19 | **Spec**: [spec.md](spec.md)

**Input**: Feature specification from `specs/004-local-gui/spec.md`

## Summary

Add a thin local Gradio Blocks interface over `whispertube.pipeline.run_pipeline`. Keep request/result
mapping as framework-independent Python so deterministic tests can prove state, path, error, and privacy
contracts. Pin the current stable Gradio 6.27.0 separately from Apple-Silicon inference dependencies.

## Technical Context

**Language/Version**: Python 3.10+; development Python 3.13, CI Python 3.12

**Primary Dependencies**: Gradio 6.27.0; existing yt-dlp, mlx-whisper, OpenCC, and ffmpeg runtime

**Storage**: Existing ignored `temp/pipeline-audio/` and `temp/pipeline-transcripts/`; local Gradio cache only

**Testing**: Python `unittest`, injected pipeline seam, real Gradio component/config inspection, local browser smoke

**Target Platform**: macOS Apple Silicon with a loopback browser UI

**Project Type**: Python package with CLI and local web GUI entry points

**Performance Goals**: UI enters running state before long pipeline work; one active job; no additional pipeline SLA

**Constraints**: Loopback-only, no share tunnel, telemetry, monitoring, hosted processing, arbitrary file exposure,
or pipeline reimplementation; preserve v0.1-v0.3 cleanup and errors

**Scale/Scope**: One local user, one URL, one active run, one preview/downloadable Markdown artifact

## Constitution Check

- PASS — pipeline and artifacts remain local; Gradio analytics and monitoring are explicitly disabled.
- PASS — the UI imports and injects the approved pipeline rather than duplicating stage logic.
- PASS — behavior tasks require RED → GREEN → REFACTOR and deterministic tests run in CI.
- PASS — one small local interface slice; packaging, cloud hosting, accounts, and richer features remain out of scope.
- PASS — real browser and Apple Silicon smoke evidence is required before review.

Post-design re-check: PASS. File exposure is bounded to validated Markdown under the configured transcript
root, event API exposure is disabled, the server binds to `127.0.0.1`, and no constitution exception is needed.

## Project Structure

### Documentation (this feature)

```text
specs/004-local-gui/
├── spec.md
├── plan.md
├── research.md
├── data-model.md
├── quickstart.md
├── contracts/
│   └── ui.md
├── checklists/
│   ├── requirements.md
│   ├── security.md
│   └── ux.md
└── tasks.md
```

### Source Code (repository root)

```text
whispertube/
├── pipeline.py
└── gui.py

tests/
├── test_pipeline.py
└── test_gui.py

requirements-ui.txt
.github/workflows/test.yml
```

**Structure Decision**: One `whispertube.gui` module owns framework-independent request/result adaptation,
Gradio Blocks construction, and local launch configuration. Existing pipeline modules remain unchanged.

## Complexity Tracking

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| None | N/A | The existing single-package structure supports the feature. |
