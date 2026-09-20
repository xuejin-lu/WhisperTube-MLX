# Implementation Plan: Downloader-Only Pivot

**Branch**: `main` | **Date**: 2026-09-21 | **Spec**: [spec.md](spec.md)

**Input**: Feature specification from `/specs/007-downloader-only-pivot/spec.md`

## Summary

Replace the former transcription GUI as the active product with one small, local
downloader workflow. A standard-library Python module will classify one explicit
YouTube video or playlist URL, build a safe yt-dlp argv list, stream yt-dlp's
progress, and print a final summary. A double-clickable `DownloadAudio.command`
will run the project-managed virtual environment and prompt for the URL. The
historical transcription/GUI implementation remains available in Git history and
the v1.0.0 tag, but is removed from the normal mainline setup and documentation.

## Technical Context

**Language/Version**: Python 3.10+

**Primary Dependencies**: yt-dlp 2026.08.19 as a project-managed CLI; Python standard library for the wrapper

**Storage**: Local audio files under `~/Downloads/WhisperTube/`; no database

**Testing**: Python `unittest`, shell launcher subprocess tests, mocked yt-dlp integration tests, real Apple Silicon smoke tests

**Target Platform**: macOS Apple Silicon; deterministic CI remains platform-neutral

**Project Type**: Local CLI plus double-click macOS launcher

**Performance Goals**: Do not buffer media in Python; delegate streaming/download work to yt-dlp

**Constraints**: no transcription, MLX, OpenCC, Gradio, localhost server, Colab automation, MP3 re-encoding, telemetry, credentials in the repository, or destructive setup cleanup

**Scale/Scope**: one interactive URL per invocation; a playlist may contain many yt-dlp-managed entries and must continue after individual failures when supported

## Constitution Check

All constitution principles pass:

- Local-first and privacy-first: media and optional browser cookies stay on the Mac.
- Spec-before-implementation and TDD: tests precede behavior changes.
- Reliability before UI: the only UI is a thin shell around the downloader.
- Small vertical slices: URL dispatch, command construction, runner, launcher, and docs are independently testable.
- No fake verification: live single-video and playlist smoke results will only be recorded after Codex runs them.
- No unnecessary human labor: setup, tests, smoke tests, git, and CI are agent-run.

## Project Structure

### Documentation (this feature)

```text
specs/007-downloader-only-pivot/
├── plan.md
├── research.md
├── data-model.md
├── quickstart.md
├── contracts/downloader.md
├── checklists/security.md
└── tasks.md
```

### Source Code (repository root)

```text
DownloadAudio.command          # Finder entry point
scripts/
├── setup_macos.sh              # create/reuse .venv and install yt-dlp only
└── launch_macos.sh             # terminal-equivalent launcher
whispertube/
└── downloader.py               # URL classification, argv construction, runner, CLI
tests/
└── test_downloader.py          # deterministic unit/integration/launcher contract tests
```

**Structure Decision**: Use one Python module and two shell entry points. Remove
the old GUI/pipeline/transcription modules and their tests from the active mainline
because the spec explicitly makes them out of scope; v1.0.0 and Git history remain
the historical access path. Keep `whispertube.youtube` out of the normal workflow
by replacing it with the downloader module rather than maintaining two product
entry points.

## Complexity Tracking

No constitution violations. The deliberate deletion of the former active GUI and
transcription path is a scope simplification required by the new product definition,
not an added architectural complexity.
