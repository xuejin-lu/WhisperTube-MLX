# Quickstart: Downloader-Only Pivot

## Prerequisites

- Apple Silicon macOS for the supported local workflow.
- Native Python 3.10 or newer.
- Network access to YouTube.
- No browser login is required for the anonymous path.

## Setup

From the repository root:

```bash
./scripts/setup_macos.sh
```

The setup creates or reuses `.venv` and installs only the pinned yt-dlp package.
It does not remove user files, cookies, downloads, or caches.

## Normal use

Double-click `DownloadAudio.command`, paste one video or explicit playlist URL,
and press Return. Files are written below `~/Downloads/WhisperTube/`.

The terminal-equivalent form is:

```bash
./scripts/launch_macos.sh 'https://www.youtube.com/watch?v=VIDEO_ID'
./scripts/launch_macos.sh 'https://www.youtube.com/playlist?list=PLAYLIST_ID'
```

For an authentication-required request, opt in explicitly:

```bash
./scripts/launch_macos.sh --cookies-from-browser safari 'https://www.youtube.com/watch?v=VIDEO_ID'
```

## Deterministic validation

```bash
./.venv/bin/python -m unittest discover -s tests -v
git diff --check
```

The deterministic suite must not contact YouTube and must not create audio files.

## Smoke validation

Use a non-sensitive approved public video and a small public playlist with an
absolute temporary output root. Confirm audio files are present, extensions are
not forced to `.mp3`, playlist names start with numeric order, and no transcript,
GUI, localhost server, or Colab upload is created. Remove the temporary smoke
directory after inspection; never commit its contents.
