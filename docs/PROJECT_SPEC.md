# WhisperTube-MLX — Project Specification

## 1. Product goal

Build a free, local-first YouTube transcription app for Apple Silicon Macs.

Primary user flow:

1. Paste a YouTube video URL.
2. Acquire the video's best available audio locally with `yt-dlp`.
3. Transcribe locally with an MLX-based Whisper implementation.
4. Convert Chinese output to Taiwan Traditional Chinese.
5. Format into readable paragraphs.
6. Save/download a Markdown transcript.

The project should eventually be usable by non-technical users without needing Terminal commands.

## 2. Target platform

Initial supported platform:

- macOS on Apple Silicon (M1/M2/M3/M4 family)

Initial development machine assumptions:

- macOS
- Homebrew available or installable
- Python environment available
- local browser session available when YouTube authentication is required

Do not optimize for Windows, Linux, Intel Mac, Colab, or hosted GPU deployment in the first milestone series.

## 3. Product principles

### Local-first

Audio download, transcription, post-processing, and transcript generation should run on the user's Mac.

### Privacy

Do not upload media, cookies, transcripts, or account credentials to third-party services by default.

### Simple UX

The final app should minimize visible technical controls. Normal use should eventually be approximately:

`open app -> paste URL -> click Transcribe -> download/copy Markdown`

### Free/open tooling

Prefer free and open-source dependencies. Do not introduce paid APIs as a normal dependency.

### Reliability before polish

Validate each pipeline stage independently before building the UI around it.

## 4. Pipeline architecture

Target pipeline:

```text
YouTube URL
   |
   v
URL validation / normalization
   |
   v
yt-dlp (local Mac network/browser context)
   |
   v
best available audio file
   |
   v
MLX Whisper (Apple Silicon)
   |
   v
raw Chinese transcript
   |
   v
OpenCC s2tw
   |
   v
paragraph formatting
   |
   v
Markdown transcript
```

## 5. YouTube acquisition strategy

The downloader must run locally.

Desired fallback behavior:

1. Try normal `yt-dlp` single-video download.
2. If YouTube requests authentication/anti-bot verification, support browser-cookie acquisition locally, preferably via `--cookies-from-browser` where supported.
3. Never require committing/exporting cookies into the repository.

For a URL such as:

`https://www.youtube.com/watch?v=VIDEO_ID&list=PLAYLIST_ID&index=2`

the initial product behavior is to transcribe only the current single video, not the entire playlist.

Downloaded audio is temporary runtime data and must not be committed.

## 6. Transcription strategy

Use an MLX-compatible Whisper implementation suitable for Apple Silicon.

Preferred quality target:

- Whisper `large-v3` where practical

The exact MLX package/API must be verified during implementation rather than assumed. If the preferred implementation changes upstream, document the selected dependency and rationale.

Initial transcription requirements:

- Chinese transcription
- no diarization requirement
- no word-level timestamps requirement
- no summarization
- no rewriting of semantic content

## 7. Text output

Post-processing requirements:

- convert Simplified Chinese to Taiwan Traditional Chinese using OpenCC `s2tw` or a documented equivalent;
- group transcript into readable paragraphs, initially targeting roughly 500 Chinese characters per paragraph;
- preserve transcript meaning; do not summarize;
- emit UTF-8 Markdown.

Suggested Markdown structure:

```markdown
# <video title>

## Source

<YouTube URL>

## Transcript

<paragraphs>
```

## 8. UI direction

Do not build the graphical UI until the local pipeline works end-to-end from Terminal/Python.

Initial UI candidate: local Gradio or another lightweight local web UI.

Later packaging may turn the project into a one-click macOS app, but native packaging is not required for early milestones.

## 9. Milestones

### v0.1 — Local YouTube audio acquisition

Goal: reliably acquire audio from one YouTube video on the maintainer's Mac.

Acceptance criteria:

- accepts a single YouTube video URL;
- downloads best available audio to a temporary/local ignored path;
- URL containing playlist parameters still processes only the current video;
- provides a documented fallback for local browser cookies if anonymous access is blocked;
- downloaded media is ignored by Git;
- core downloader logic is testable without requiring a live YouTube request where possible.

### v0.2 — Local MLX transcription

Goal: transcribe a local audio file using Apple Silicon acceleration.

Acceptance criteria:

- local audio file -> Chinese transcript;
- selected MLX Whisper dependency and model are documented;
- basic error messages for missing model/dependency/input;
- one UTF-8 Markdown transcript with Taiwan Traditional Chinese text grouped
  into readable paragraphs;
- no cloud transcription dependency.

### v0.3 — End-to-end CLI pipeline

Goal:

`YouTube URL -> audio -> Whisper -> Traditional Chinese -> Markdown`

Acceptance criteria:

- one command/function runs the full pipeline;
- temporary audio cleanup behavior is defined;
- Markdown output is generated;
- error source is distinguishable (download vs transcription vs output).

Implementation note: the pipeline reuses the approved acquisition and transcription
boundaries, owns only current-run temporary audio, cleans that audio after success or
transcription failure, and never treats the transcript as cleanup-eligible.

### v0.4 — Local graphical UI

Goal: minimal interface for non-technical use.

Acceptance criteria:

- URL textbox;
- Start/Transcribe button;
- visible progress/status;
- transcript preview;
- Markdown download;
- runs locally and does not create a public tunnel by default.

### v1.0 — Public usable release

Goal: reasonable installation and usage flow for other Apple Silicon Mac users.

Potential deliverables:

- installation script or packaged app;
- clear README;
- troubleshooting guide;
- versioned GitHub Release.

## 10. Explicit non-goals for early development

Do not add these before the core pipeline is stable:

- playlist batch transcription;
- speaker diarization;
- timestamps/word alignment;
- summaries/LLM post-processing;
- hosted cloud service;
- user accounts;
- database;
- analytics/telemetry;
- Windows/Linux support;
- paid API fallback;
- complex plugin architecture.

## 11. Security / repository rules

Never commit:

- `cookies.txt` or browser session exports;
- `.env` secrets;
- downloaded YouTube media;
- user recordings;
- generated private transcripts;
- model caches.

Treat browser cookies as credentials.

## 12. Current test video

During v0.1 development, the maintainer has been using this public YouTube video as a reproducible test case:

`https://www.youtube.com/watch?v=gmj41fQTbfY`

This URL is test data, not a product dependency.
