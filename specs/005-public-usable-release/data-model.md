# Data Model: Public Usable Release

This feature adds no persistent database. The model describes release configuration and local runtime ownership so setup and documentation can be tested against explicit boundaries.

## Release Configuration

| Field | Type | Meaning | Safety rule |
|---|---|---|---|
| `version` | string | v1.0 release identifier | Must match `VERSION`, importable metadata, docs, and release plan |
| `project_root` | path | Checkout or unpacked source root | Derived from scripts; never hard-coded to a maintainer path |
| `venv_path` | path | Project-local Python environment | Defaults to `<project_root>/.venv`; disposable and ignored |
| `requirements` | paths | Pinned Python dependency inputs | Read from tracked requirement files; no remote unpinned install input |
| `python_executable` | path | Native Python used for setup/launch | Must report `arm64` on supported macOS |
| `ffmpeg_executable` | path | Local decoder required by pipeline | Must be found on `PATH`; setup reports remediation if absent |
| `default_model` | string | Normal transcription quality target | `mlx-community/whisper-large-v3-mlx` remains unchanged |
| `smoke_model` | string | Explicit small validation model | `mlx-community/whisper-tiny`; never silently replaces the default |
| `audio_dir` | path | Current-run/project-local acquired audio | Must stay in approved ignored runtime roots |
| `output_dir` | path | Retained Markdown transcripts | Must stay in approved ignored/local output roots |
| `loopback_host` | string | GUI bind address | Must be `127.0.0.1`; no public share/tunnel |

## Local Runtime Artifact

| Artifact | Owner | Default location | Retention | Repository rule |
|---|---|---|---|---|
| Virtual environment | Setup path | `<project_root>/.venv` | Until user removes/recreates it | Ignored; never committed |
| Current-run audio | Pipeline | `<project_root>/temp/...` | Removed after run according to v0.3 rules | Ignored; never committed |
| Markdown transcript | Pipeline/user | `<project_root>/outputs/...` or approved local output | Retained until user removes it | Ignored; never committed |
| Model cache | MLX/underlying model loader | User-local model cache outside checkout | Retained across runs unless user explicitly removes it | Never bundled or committed |
| Cookies/browser profile | User/browser | Browser-managed location | Never copied by release paths | Never read/exported/committed by setup or release artifacts |
| Release logs | Script/process | Terminal or explicitly selected local path | User-controlled | Must not contain secrets or absolute maintainer paths |

## Release Candidate

The candidate is the tuple `{version, source_commit, deterministic_test_result, ci_run, apple_silicon_smoke, artifact_inspection, release_notes_draft}`. It is reviewable but not published until the explicit release approval.
