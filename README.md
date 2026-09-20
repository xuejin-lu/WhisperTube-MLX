# WhisperTube-MLX

WhisperTube downloads the best available audio from one YouTube video or
playlist for manual use elsewhere, such as Google Colab. It does not transcribe,
upload, summarize, or run a local web server.

## Normal use on Apple Silicon macOS

Requirements:

- native Python 3.10 or newer;
- a network connection to YouTube;
- no browser login for the normal anonymous path.

From the repository root, run setup once:

```bash
./scripts/setup_macos.sh
```

Then double-click `DownloadAudio.command` in Finder, paste one YouTube URL, and
press Return. Audio files are saved under:

```text
~/Downloads/WhisperTube/
```

The terminal-equivalent command is:

```bash
./scripts/launch_macos.sh 'https://www.youtube.com/watch?v=VIDEO_ID'
./scripts/launch_macos.sh 'https://www.youtube.com/playlist?list=PLAYLIST_ID'
```

The setup creates or reuses `.venv` and installs only the pinned yt-dlp runtime.
It does not delete downloads, cookies, or caches. The launcher resolves the
repository path safely even when it contains spaces and uses the project-managed
yt-dlp executable.

## Video and playlist behavior

- A watch, short, live, embed, or `youtu.be` URL downloads one video.
- A URL whose path is explicitly `/playlist?list=...` downloads the playlist.
- A watch URL that merely contains `list=` remains a single-video request.
- Video files use `%(title)s [%(id)s].%(ext)s`.
- Playlist files use a playlist directory and numeric order:
  `%(playlist_index)03d - %(title)s [%(id)s].%(ext)s`.
- yt-dlp selects `bestaudio`; files keep their source extension such as `.webm`
  or `.m4a`. No MP3 conversion is performed.
- Individual unavailable playlist entries are skipped when yt-dlp supports
  continuation, and the terminal prints downloaded/failed counts plus the output
  directory.

## Optional browser-cookie retry

Anonymous download is always attempted by default. If YouTube requires local
browser authentication, opt in explicitly:

```bash
./scripts/launch_macos.sh \
  --cookies-from-browser safari \
  'https://www.youtube.com/watch?v=VIDEO_ID'
```

Cookies remain local to the browser and are never exported to this repository or
sent to Colab. WhisperTube never opens a browser or captures credentials.

## Verification

Run deterministic tests without contacting YouTube:

```bash
./.venv/bin/python -m unittest discover -s tests -v
git diff --check
```

For local smoke validation, use an approved public video and a small public
playlist with a safe temporary output root. Confirm that audio files are created,
playlist names are numerically ordered, no transcript or server appears, and no
media is committed.

## Historical release

The v1.0.0 tag is historical evidence of the former local transcription product.
The current `main` workflow is intentionally downloader-only. Transcription,
MLX, OpenCC, Gradio, Colab automation, database, telemetry, code signing, and
`.app` packaging are outside the current product scope.
