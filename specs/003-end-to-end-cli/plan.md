# Implementation Plan: End-to-End CLI Pipeline

**Branch**: `003-end-to-end-cli` | **Date**: 2026-09-19 | **Spec**: [spec.md](spec.md)

## Summary

Add one orchestration module/CLI that calls approved v0.1 acquisition then approved v0.2
transcription. It owns only current-run temporary audio cleanup and pipeline error wrapping.

## Technical Context

**Language/Version**: Python 3.10+ (development target 3.11+)

**Primary Dependencies**: Existing yt-dlp, mlx-whisper, OpenCC, and ffmpeg; no new package.

**Storage**: Ignored `temp/pipeline-audio/` and existing ignored transcript dirs.

**Testing**: Python `unittest` with injected acquisition/transcription functions.

**Target Platform**: macOS Apple Silicon

**Project Type**: Python CLI and reusable module

**Performance Goals**: One single-video run; local smoke records timing rather than enforcing SLA.

**Constraints**: Local/private; reuse approved boundaries; clean only acquired audio; preserve causes;
no YouTube/model/hardware work in CI; no silent overwrite.

**Scale/Scope**: One URL, one audio file, one Markdown artifact; no GUI, batch, or cloud.

## Constitution Check

- PASS — local ignored artifacts only; no credentials/telemetry.
- PASS — injected stage tests keep CI deterministic.
- PASS — existing boundaries remain authoritative and errors actionable.
- PASS — one small orchestration slice; v0.1/v0.2 remain unchanged.

## Project Structure

```text
whispertube/
├── youtube.py
├── transcription.py
└── pipeline.py

tests/
└── test_pipeline.py

specs/003-end-to-end-cli/
├── spec.md
├── plan.md
├── research.md
├── data-model.md
├── contracts/cli.md
├── quickstart.md
└── tasks.md
```

**Structure Decision**: one injected orchestration module avoids duplicated stage logic.

## Complexity Tracking

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| None | N/A | Existing package supports one module. |
