# Feature Specification: Downloader-Only Pivot

**Feature ID**: 007-downloader-only-pivot  
**Target**: product simplification / new mainline direction  
**Status**: Ready for Spec Kit planning and implementation

## 1. Product definition

WhisperTube is no longer a local transcription application.

The product now has one purpose:

> Given one YouTube video URL or one YouTube playlist URL, download the best available audio files to a predictable local folder for manual upload to Colab.

The Mac is used only as the YouTube acquisition machine. Transcription is outside the product.

## 2. Primary user flow

```text
Double-click DownloadAudio.command
        |
        v
Paste one YouTube video or playlist URL
        |
        v
Download best available audio
        |
        v
Save under ~/Downloads/WhisperTube/
        |
        v
User manually uploads audio files to Colab
```

No transcription happens in this repository.

## 3. In scope

- One explicit YouTube video URL.
- One explicit YouTube playlist URL.
- Best available audio-only download via yt-dlp.
- Preserve source audio format when practical; do not re-encode to MP3.
- Predictable local output under:
  `~/Downloads/WhisperTube/`
- Single-video output with title and video ID.
- Playlist output in a playlist-named directory.
- Playlist filenames prefixed with playlist order.
- Continue downloading later playlist entries when an individual item fails.
- Clear terminal progress and final summary.
- Anonymous download first.
- Optional local browser-cookie retry/fallback when YouTube requires authentication.
- A double-clickable macOS launcher, `DownloadAudio.command`.
- Deterministic tests for URL classification, command construction, output naming, playlist behavior, and failure handling.

## 4. Out of scope

The following are explicitly forbidden in this feature:

- Gradio.
- Web GUI.
- Local HTTP server.
- MLX.
- Whisper.
- OpenCC.
- Any transcription.
- Any transcript cleanup or correction.
- CUDA.
- Colab integration.
- Automatic file upload.
- Google Drive integration.
- LLM summarization.
- Diarization.
- Timestamps.
- Subtitle generation.
- Audio-to-MP3 conversion.
- macOS .app packaging.
- Code signing or notarization.
- Background service / daemon.
- Cloud backend.
- Database.
- Telemetry.

The v1.0.0 release remains historical evidence of the older product direction and must not be rewritten.

## 5. URL behavior

### 5.1 Single video

Accept explicit single-video URLs such as:

- `https://www.youtube.com/watch?v=VIDEO_ID`
- `https://youtu.be/VIDEO_ID`
- YouTube Shorts / live / embed forms already supported by the current normalizer.

For a single-video request:

- download exactly one video's best available audio;
- do not accidentally traverse a playlist merely because the watch URL contains a `list=` query parameter;
- save using a deterministic template such as:
  `%(title)s [%(id)s].%(ext)s`

### 5.2 Playlist

Accept explicit playlist URLs such as:

`https://www.youtube.com/playlist?list=PLAYLIST_ID`

For a playlist request:

- use yt-dlp playlist mode;
- download every available playlist item;
- continue past unavailable/private/failed entries when possible;
- preserve playlist order in filenames using `playlist_index`;
- save under:
  `~/Downloads/WhisperTube/<playlist name>/`
- use a deterministic template such as:
  `%(playlist_index)03d - %(title)s [%(id)s].%(ext)s`

A normal watch URL that merely contains `list=` must still be treated as a single-video request unless it is an explicit playlist URL.

## 6. Audio format

Use yt-dlp best-audio selection:

```text
-f bestaudio
```

Do not re-encode the media after download.

Expected output may therefore be formats such as:

- `.webm`
- `.m4a`

The downloader must not force MP3.

## 7. Output root

Default output root:

```text
~/Downloads/WhisperTube/
```

Examples:

Single video:

```text
~/Downloads/WhisperTube/
└── Predicate Logic I [abc123].webm
```

Playlist:

```text
~/Downloads/WhisperTube/
└── Predicate Logic/
    ├── 001 - Predicate Logic I [abc123].webm
    ├── 002 - Predicate Logic II [def456].webm
    └── 003 - Predicate Logic III [ghi789].m4a
```

Do not require the user to understand repository-relative `temp/` or `outputs/` directories for normal usage.

## 8. macOS launcher

Add a double-clickable:

```text
DownloadAudio.command
```

Normal interaction:

```text
Paste YouTube video or playlist URL:
> ...
```

Then download immediately.

The launcher must:

- resolve the repository path safely even if it contains spaces;
- use the project-managed yt-dlp if the repository setup provides one;
- print clear errors if required dependencies are missing;
- print actionable errors and return non-zero for invalid URLs, missing yt-dlp,
  unwritable output, and unexpected yt-dlp failures before or during a download;
- not launch a browser or local server;
- not invoke transcription code.

## 9. Setup simplification

The normal setup path should install only what the downloader needs.

The implementation should determine the smallest maintained dependency set.

Expected direction:

- Python only if still needed by the thin wrapper;
- yt-dlp;
- ffmpeg only if yt-dlp genuinely requires it for selected audio extraction/merging behavior.

Remove MLX Whisper, OpenCC, and Gradio from the active normal setup requirements.

Do not delete historical release artifacts or tags.

## 10. Cookie fallback

Default behavior:

```text
anonymous yt-dlp
```

When YouTube blocks the request and local browser authentication is appropriate, support an explicit browser-cookie option, e.g.:

```text
--cookies-from-browser safari
```

Requirements:

- cookies remain local;
- no cookies are exported into the repository;
- no cookies are sent to Colab;
- do not automate browser credential capture.

The feature may expose cookie fallback as an optional CLI flag or a clear retry path. It must not silently use browser cookies on every request.

## 11. Playlist failure behavior

A playlist must not fail the entire batch solely because one entry is unavailable.

Preferred behavior:

```text
[1/24] downloaded
[2/24] downloaded
[3/24] unavailable - skipped
[4/24] downloaded
...
```

At completion, print a concise summary:

```text
Downloaded: 23
Failed/skipped: 1
Output: ~/Downloads/WhisperTube/Predicate Logic/
```

Use yt-dlp's supported error-continuation behavior rather than reimplementing playlist traversal unless a wrapper is required for reporting.

## 12. Preserve history, simplify mainline

Existing components such as:

- `whispertube/transcription.py`
- `whispertube/pipeline.py`
- `whispertube/gui.py`
- MLX / Gradio requirements
- `WhisperTube.command`

belong to the previous product direction.

Codex must decide through the plan whether to:

1. remove them from current `main`; or
2. leave them present but clearly deprecated and unreachable from the normal workflow.

Preference: reduce active code and dependencies aggressively while preserving historical access through Git history and tag `v1.0.0`.

Do not maintain two competing primary product paths.

## 13. Tests

Deterministic tests must cover at minimum:

- explicit video URL classification;
- explicit playlist URL classification;
- watch URL with `list=` remains single-video;
- short / Shorts / embed / live normalization as relevant;
- video command includes best-audio and single-video behavior;
- playlist command includes playlist behavior and indexed naming;
- no MP3 re-encoding flags;
- output root defaults to `~/Downloads/WhisperTube/`;
- playlist output path/template is deterministic;
- path-with-spaces launcher behavior;
- missing yt-dlp produces a clear error;
- browser-cookie option is passed only when explicitly requested;
- no transcription/MLX/Gradio module is invoked by the normal workflow;
- no playlist failure behavior accidentally stops all later entries when yt-dlp supports continuation.

CI must not hit live YouTube.

## 14. Real smoke tests

After deterministic tests pass, perform real Apple Silicon smoke verification:

### Single video
- use an approved public test video;
- confirm one audio file is created;
- confirm no transcript is created;
- confirm no local server starts.

### Playlist
- use a small public playlist suitable for testing;
- confirm multiple audio files are created;
- confirm numeric playlist ordering is reflected in filenames;
- confirm output lands below `~/Downloads/WhisperTube/` or a safe temporary override for test isolation;
- confirm no transcription dependency is imported or executed.

Do not commit downloaded media.

## 15. Documentation

Rewrite the primary README around the new product definition.

The first-screen documentation should say:

```text
WhisperTube downloads audio from a YouTube video or playlist for manual use elsewhere, such as Google Colab.
```

Normal use:

```text
1. Double-click DownloadAudio.command
2. Paste a YouTube video or playlist URL
3. Wait for audio download
4. Open ~/Downloads/WhisperTube/
5. Manually upload the files to Colab
```

Do not present local transcription, privacy-first inference, Apple Silicon MLX, or Gradio as current product advantages.

Historical documentation may remain under versioned release/tag history rather than dominating current README.

## 16. Acceptance criteria

Feature 007 is complete when:

- the normal workflow has no transcription step;
- one double-click launcher accepts one URL;
- both single-video and explicit-playlist URLs work;
- playlist items are downloaded in order with deterministic names;
- best available audio is preserved without MP3 re-encoding;
- output goes to a predictable user Downloads directory;
- one failed playlist item does not unnecessarily abort the full playlist;
- no MLX, Whisper, OpenCC, Gradio, localhost server, or Colab automation is required;
- deterministic tests and CI pass;
- real single-video and playlist smoke tests pass;
- README and STATUS describe the downloader-only product;
- no new GitHub Release or tag is published without separate review.

## 17. Codex workflow

On the next `開始`:

1. sync/rebase to current `origin/main`;
2. read `AGENTS.md`, `docs/STATUS.md`, and this feature spec;
3. run Spec Kit clarify/plan/checklist/tasks/analyze as appropriate;
4. prefer deletion/deprecation over preserving unnecessary product complexity;
5. implement with TDD;
6. preserve only the downloader functionality required by this spec;
7. run focused and full deterministic tests;
8. run real single-video and playlist smoke tests;
9. run `git diff --check` and `$speckit-converge`;
10. update README and `docs/STATUS.md`;
11. commit, push, verify exact-HEAD CI;
12. stop for repository review.

Do not publish a release or begin transcription/Colab work.
