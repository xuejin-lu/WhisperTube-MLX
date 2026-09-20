# Feature Specification: Local Audio Input

**Feature ID**: 006-local-media-input  
**Target**: post-v1.0 usability feature (candidate for v1.1)  
**Status**: Ready for Spec Kit planning and implementation

## 1. Goal

Extend the existing local Gradio GUI so a user can transcribe either:

1. one YouTube URL using the already approved v0.3 pipeline; or
2. one local audio file using the already approved local transcription boundary.

The normal user flow becomes:

```text
Open WhisperTube.command
        |
        v
Paste one YouTube URL
        OR
Choose one local audio file
        |
        v
Transcribe
        |
        v
Traditional Chinese Markdown preview + download
```

This feature must reuse the existing transcription implementation rather than creating a second Whisper path.

## 2. Scope

### In scope

- Add a local-audio file picker to the existing GUI.
- Keep the existing YouTube URL workflow unchanged.
- Route a local audio selection directly to `whispertube.transcription.transcribe_audio()` or an equivalent shared approved boundary.
- Support the audio suffixes already approved by the transcription module:
  - `.aac`
  - `.flac`
  - `.m4a`
  - `.mp3`
  - `.ogg`
  - `.wav`
  - `.webm`
- Preserve Taiwan Traditional Chinese conversion, paragraph formatting, Markdown preview, and Markdown download.
- Preserve the existing default model `mlx-community/whisper-large-v3-mlx`.
- Preserve the existing smaller explicit model override for smoke tests.
- Preserve loopback-only GUI behavior and all v0.4 file-serving/privacy boundaries.

### Out of scope

- Local video containers such as `.mp4`, `.mov`, or `.mkv`.
- Multiple-file or batch transcription.
- Playlist transcription.
- Dragging an entire folder.
- Speaker diarization.
- Timestamps / word alignment.
- Summarization or LLM rewriting.
- Editing the source audio.
- Deleting, moving, renaming, or overwriting the user's original local audio file.
- Cloud upload or hosted transcription.
- A new public release/tag until this feature is separately reviewed.

## 3. User stories

### US1 — Transcribe a local audio file

As a user, I can choose one supported local audio file in the same GUI I already use for YouTube and receive a Taiwan Traditional Chinese Markdown transcript.

Acceptance:

- Given a readable supported local audio file,
- when I select it and press **Transcribe**,
- then WhisperTube skips yt-dlp,
- transcribes locally with the selected/default MLX Whisper model,
- produces a validated non-empty UTF-8 Markdown transcript,
- previews the transcript,
- and offers the exact validated Markdown artifact for download.

### US2 — Preserve the original file

As a user, my original local audio must never be treated as disposable pipeline audio.

Acceptance:

- Success, transcription failure, GUI failure, cleanup, app restart, or cancellation MUST NOT delete, truncate, move, rename, or overwrite the user's original local audio file.
- If Gradio creates its own temporary upload/cache copy, cleanup may affect only that framework-owned copy according to documented framework behavior, never the original source file.

### US3 — Keep YouTube behavior unchanged

As an existing user, I can still paste one YouTube URL and use the already approved URL pipeline exactly as before.

Acceptance:

- Local-audio support MUST NOT bypass or weaken existing URL validation, yt-dlp behavior, temporary-audio cleanup, error categories, transcript validation, or file-serving protections.

## 4. Input-selection contract

The GUI MUST expose two mutually exclusive input routes:

- **YouTube URL**
- **Local audio file**

Exactly one route must be selected for a transcription request.

Required behavior:

- URL only -> run the existing YouTube pipeline.
- Local audio only -> run local transcription directly.
- Neither -> clear input error; no transcription/download call.
- Both -> clear input error asking the user to choose exactly one; neither backend may run.

The GUI must not silently prefer one input over the other.

## 5. Local-audio validation

Before local transcription:

- the selected file must exist;
- it must be a regular readable file;
- its suffix must be one of the currently approved transcription suffixes;
- unsupported formats must produce an input error before model inference;
- no arbitrary directory may be exposed through Gradio file serving.

Do not duplicate the transcription module's canonical validation rules if they can be safely reused.

## 6. File ownership and privacy

The following are hard requirements:

- The user's original local file is user-owned and cleanup-ineligible.
- The YouTube-acquired current-run audio remains app-owned temporary data and follows the existing v0.3 cleanup contract.
- Generated transcripts remain under an approved ignored runtime output root.
- The GUI must continue to expose only the validated Markdown result through Gradio's controlled output/cache mechanism.
- Do not add a broad `allowed_paths` directory.
- Continue rejecting ambient `GRADIO_ALLOWED_PATHS`.
- No audio, transcript, browser cookie, model cache, or local absolute path may be committed to the repository.
- No local audio is uploaded to an external service.

## 7. Error behavior

The GUI must preserve cause-specific safe errors.

Examples:

- neither/both inputs -> `input error`
- unsupported/missing/unreadable local file -> `input error`
- ffmpeg missing -> `dependency error`
- model load failure -> `model error`
- MLX/decode/transcription failure -> `inference error`
- transcript write/validation failure -> `output error`

Unexpected exceptions must remain sanitized and must not reveal private absolute paths, cookies, credentials, or tracebacks in the browser.

## 8. GUI behavior

The existing one-action interface should remain simple.

Minimum layout:

```text
YouTube URL
[____________________________]

or

Local audio
[ Choose File ]

[ Transcribe ]

Status
Transcript preview
Download Markdown
```

Requirements:

- one visible Transcribe action;
- running state disables duplicate active work;
- terminal success/error re-enables the action;
- beginning a new run clears stale preview/download state;
- file-picker labeling must make it clear that local audio stays local;
- keyboard/browser usability from v0.4 must not regress.

## 9. Output behavior

For either input route:

- output is UTF-8 Markdown;
- text is Taiwan Traditional Chinese using the existing `s2tw` path;
- paragraph formatting uses the existing approved implementation;
- preview bytes/text correspond to the validated generated Markdown;
- the downloadable result is the validated transcript artifact or the framework-controlled safe copy of it.

For repeated local transcription of a file with the same basename, the implementation must choose and document one safe deterministic behavior:

1. generate a non-destructive unique output filename; or
2. return a clear output collision error.

It MUST NOT overwrite an existing transcript silently.

## 10. Deterministic tests

Before implementation is considered complete, tests must cover at least:

- URL only dispatches exactly once to the existing pipeline.
- Local file only dispatches exactly once to the local transcription boundary and does not invoke yt-dlp/pipeline acquisition.
- Neither input -> no backend call.
- Both inputs -> no backend call.
- Every currently approved suffix is accepted by the local route or delegated to canonical validation.
- Unsupported suffix is rejected before inference.
- Original local audio remains byte-identical and present after:
  - success;
  - transcription failure;
  - output failure.
- Existing YouTube cleanup tests continue to pass.
- Existing direct-file-route privacy test continues to return HTTP 403 for unrelated files.
- Valid local transcript preview/download remain byte-identical.
- Unexpected local-path-containing exception is sanitized.
- Full deterministic repository suite passes.

CI must remain independent of live YouTube, model downloads, and Apple-Silicon-only inference by using fakes/mocks where appropriate.

## 11. Real Apple Silicon smoke

After deterministic tests pass, perform one real local smoke using a small explicit model such as `mlx-community/whisper-tiny` and a maintainer-owned/non-sensitive local audio fixture outside tracked source.

Record only non-sensitive evidence:

- suffix/type used;
- model used;
- successful non-empty Markdown result;
- original source still exists and is unchanged;
- no yt-dlp acquisition occurred for the local route;
- loopback-only GUI remained local;
- no public share URL;
- no source audio or transcript committed.

Do not record or commit the audio content itself.

## 12. Documentation

Update the README/user-facing instructions so normal use is described as:

```text
Double-click WhisperTube.command
-> paste YouTube URL OR choose local audio
-> Transcribe
-> preview/download Markdown
```

Document the supported local audio suffixes and explicitly state that local video files are not yet supported.

## 13. Review gates

Codex must use the repository's Spec Kit + TDD workflow:

1. sync/rebase to current `origin/main`;
2. run Spec Kit clarify/plan/checklist/tasks/analyze as appropriate;
3. resolve generated checklist items under the existing reviewer policy;
4. RED -> GREEN -> REFACTOR for the smallest implementation slices;
5. run focused and full deterministic tests;
6. perform the real Apple Silicon local-audio smoke;
7. run `$speckit-converge`;
8. commit, push, verify exact-HEAD CI;
9. persist review evidence in GitHub, especially `docs/STATUS.md`;
10. stop and request repository review.

Do not create a new tag or GitHub Release during this feature implementation.
