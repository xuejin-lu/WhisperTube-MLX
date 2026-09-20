# Research: Local Audio Input

## Decision: Reuse the existing transcription boundary

- **Decision**: Route local audio directly to `whispertube.transcription.transcribe_audio()`.
- **Rationale**: The existing function already validates regular readable files, approved suffixes, ffmpeg availability, model/inference errors, Taiwan Traditional Chinese conversion, output collisions, and UTF-8 Markdown writing. A second Whisper path would duplicate safety and error logic.
- **Alternatives considered**: Add a new local-media service (rejected as unnecessary abstraction); route local files through `run_pipeline()` (rejected because it would incorrectly invoke YouTube acquisition and app-owned cleanup).

## Decision: Use a single Gradio filepath input

- **Decision**: Add `gr.File(type="filepath", file_count="single", ...)` to the existing Blocks interface and pass the resulting framework-managed filepath to the local transcription boundary.
- **Rationale**: The pinned Gradio dependency already provides the file component and controlled cache behavior used by the existing output download. A single filepath preserves the one-file scope and keeps the source outside the app-owned YouTube cleanup root.
- **Alternatives considered**: Expose a broad transcript/source directory through `allowed_paths` (rejected by the v0.4 privacy contract); add a native macOS picker (rejected because it would create a second GUI integration path and is not needed for the browser-local workflow).

## Decision: Enforce mutual exclusion in the GUI handler

- **Decision**: Validate the URL/file pair before any backend call and return an input error for neither or both.
- **Rationale**: A single boundary makes the contract deterministic and prevents accidental preference for one input when both are supplied. Existing YouTube behavior remains delegated to `run_pipeline()`.
- **Alternatives considered**: Prefer URL when both are supplied (rejected because the spec requires an explicit choice); add two separate buttons (rejected because the UI contract requires one visible Transcribe action).

## Decision: Preserve source ownership through read-only behavior

- **Decision**: Do not add cleanup code for the selected local file; rely on `transcribe_audio()` reading it and writing only to the approved output root.
- **Rationale**: The source is user-owned. Tests can prove byte identity after success, inference failure, and output failure without touching the real user's file.
- **Alternatives considered**: Copy then delete the original (rejected); normalize/move the source into `temp/` (rejected because it changes ownership and violates the privacy contract).

## Decision: Keep output collision behavior explicit

- **Decision**: Retain the existing refusal to overwrite a same-stem transcript.
- **Rationale**: It is deterministic, non-destructive, and already covered by transcription tests. The GUI should surface it as an output error.
- **Alternatives considered**: Generate unique names (not needed for this slice and would change existing output expectations); overwrite (rejected by privacy/reliability constraints).

## Local evidence used

- Installed pinned Gradio configuration and existing `tests/test_gui.py` establish the current private event, loopback, cache, and file-serving seams.
- Existing `whispertube.transcription._SUPPORTED_AUDIO_SUFFIXES` is the canonical supported suffix set.
- Existing pipeline tests establish that only YouTube-acquired current-run audio is cleanup-eligible.
