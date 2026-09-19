# Implementation Plan: Public Usable Release

**Branch**: `005-public-usable-release` | **Date**: 2026-09-19 | **Spec**: [spec.md](spec.md)

## Summary

Deliver the smallest maintainable v1.0 distribution path: a versioned source release with a native-Apple-Silicon prerequisite diagnostic, an idempotent macOS setup script, a local launch script, consistent version metadata, troubleshooting/release documentation, and deterministic tests. The existing v0.1-v0.4 pipeline and GUI remain the execution core; v1.0 adds release ergonomics and validation without adding a hosted service or weakening the loopback/file-serving/privacy contracts.

## Technical Context

**Language/Version**: Python 3.10+; POSIX shell with Bash-compatible syntax for macOS scripts

**Primary Dependencies**: Existing pinned `mlx-whisper==0.4.3`, `OpenCC==1.4.2`, `gradio==6.27.0`; `yt-dlp` remains a local executable dependency; `ffmpeg` remains a Homebrew/system dependency

**Storage**: No database. `.venv/` is disposable and ignored; `temp/` and `outputs/` are project-local ignored runtime paths; model caches remain outside tracked files and are not managed by setup scripts.

**Testing**: `python -m unittest discover -s tests -v`; deterministic release/configuration tests run on CI; Apple Silicon MLX and YouTube smoke remain local-only evidence.

**Target Platform**: macOS 14+ on native Apple Silicon with a native supported Python and local `ffmpeg`; Intel macOS, Rosetta Python, Linux, and Windows are unsupported for v1.0.

**Project Type**: Local Python CLI + Gradio GUI distributed as a source release

**Performance Goals**: Setup should avoid unnecessary work on repeat runs; launch should fail fast on missing prerequisites; no new transcription latency target is introduced beyond the approved pipeline.

**Constraints**: No network service, tunnel, telemetry, account, database, package-manager auto-install, credentials collection, broad file-serving path, model bundle, or automatic GitHub Release publication. Browser login, Keychain, and macOS privacy prompts remain explicit user-owned gates if encountered; the release never bypasses or captures them.

**Scale/Scope**: One local user and one video per run; one v1.0 source-release path; no concurrent-user or server deployment target.

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- Local-first: PASS. Setup only prepares local dependencies; acquisition, inference, conversion, and output remain local.
- Privacy-first: PASS. Scripts do not read or export cookies, credentials, browser profiles, transcripts, media, or model caches; artifact checks are explicit.
- Spec-driven: PASS. This plan maps to FR-001–FR-020 and SC-001–SC-006 before implementation.
- Test-first: PASS. Release/configuration behavior gets deterministic RED → GREEN → REFACTOR tests; network/MLX claims require real smoke evidence.
- Reliability/small slices: PASS. The implementation is split into diagnostics, setup/launch, documentation/version, and release validation while preserving existing pipeline stages.

## Research Decisions

See [research.md](research.md). The key decisions are:

1. Use Python `venv` and pinned requirements rather than introducing a new package manager or application packager.
2. Require native Apple Silicon Python and macOS 14+ diagnostics before installing MLX dependencies.
3. Keep `ffmpeg` as an explicit prerequisite; do not silently install Homebrew or elevate privileges.
4. Use source release + scripts for v1.0; defer signed/notarized application packaging.
5. Treat model download/cache as local first-use behavior and never bundle or delete it automatically.

## Project Structure

### Documentation (this feature)

```text
specs/005-public-usable-release/
├── plan.md
├── research.md
├── data-model.md
├── quickstart.md
├── contracts/
│   └── release.md
└── tasks.md
```

### Source Code (repository root)

```text
README.md                         # public setup/launch path and user workflow
VERSION                           # single release version value
docs/RELEASE.md                   # candidate checklist and GitHub Release plan
docs/TROUBLESHOOTING.md           # actionable prerequisite/runtime diagnosis
scripts/setup_macos.sh            # idempotent setup and prerequisite gate
scripts/launch_macos.sh           # prepared-environment local GUI launcher
whispertube/version.py            # importable version source
whispertube/release.py            # pure diagnostics/config/version entry point
tests/test_release.py             # deterministic release-path tests
```

Existing `whispertube.pipeline`, `whispertube.transcription`, `whispertube.youtube`, and `whispertube.gui` remain the approved functional core. Existing test files remain the regression suite.

**Structure Decision**: Keep the single-project layout. Shell scripts are thin adapters around testable Python diagnostics; release metadata is plain text plus one importable constant; no new application layer or packaging framework is introduced.

## Implementation Phases

### Phase 0 — Research and contract design

- Record official guidance and repository constraints in `research.md`.
- Define release configuration, runtime-artifact ownership, retention, and privacy boundaries in `data-model.md`.
- Define setup, launch, diagnostic, and release-plan contracts in `contracts/release.md`.

### Phase 1 — Deterministic release foundation

- Add version metadata and pure host/configuration diagnostics.
- Add failing unit tests for supported/unsupported host cases, version consistency, safe paths, and diagnostic output.
- Implement the minimum diagnostics and version entry point.
- Refactor only after focused tests are green.

### Phase 2 — Setup and launch slice

- Add failing tests for setup/launch command shape, idempotent environment behavior, and failure messaging using fakes or temporary directories.
- Implement `setup_macos.sh` and `launch_macos.sh` as thin, quoted, non-destructive wrappers.
- Verify scripts are executable, path-safe, and do not auto-enable public sharing or broad file serving.

### Phase 3 — Public documentation and release readiness

- Update README with clean-checkout flow, prerequisites, version, model/cache, cleanup, and troubleshooting links.
- Add troubleshooting and release plan docs, including explicit separation of CI, local Apple Silicon smoke, and final publication approval.
- Add deterministic artifact-safety inspection coverage and ensure tracked files contain no runtime/private artifacts.

### Phase 4 — Local validation and convergence

- Run focused and full deterministic tests.
- Run the local Apple Silicon smoke using the approved public video and explicit `mlx-community/whisper-tiny` model when technically available.
- Inspect release artifacts, update `docs/STATUS.md`, run Spec Kit converge, commit coherently, push, and record CI state.

## Test Strategy

### Deterministic tests

- Pure Python tests cover version alignment, architecture/OS/Python/decoder checks via injected facts, error categories, approved local paths, and privacy-safe diagnostics.
- Script tests inspect command construction or execute scripts in a temporary fake toolchain; they do not install packages or access YouTube.
- Existing suite remains the regression test for pipeline cleanup, error classification, GUI loopback, and file-serving boundaries.

### Integration/smoke tests

- On the development Apple Silicon Mac, run the setup/launch path against the existing environment where possible without deleting it.
- Run the approved public test video through the GUI/pipeline with `mlx-community/whisper-tiny`; verify non-empty UTF-8 Markdown, current-run audio cleanup, loopback-only behavior, and no public share URL.
- Do not claim large-v3 performance or full clean-machine installation unless actually run; record skipped evidence explicitly.

## Complexity Tracking

No constitution violations. The project intentionally does not add a packaging framework, installer, service, or new external runtime.
