# WhisperTube-MLX
Local YouTube transcription app powered by MLX Whisper for Apple Silicon.

## v0.1: local audio acquisition

The first milestone provides a small Python CLI that normalizes one YouTube URL
and downloads that video's best available audio-only representation (`bestaudio`)
with local `yt-dlp`. Playlist parameters are ignored; only the current video is
downloaded.

Install `yt-dlp` on the maintainer's Mac, then run this local verification
command from the repository root:

```bash
python3 -m pip install -U yt-dlp
python3 -m whispertube.youtube \
  'https://www.youtube.com/watch?v=gmj41fQTbfY' \
  --output-dir temp/audio
```

The expected evidence is a `[download] 100%` line and an audio file under
`temp/audio/`. The directory is ignored by Git. If YouTube requires local
browser authentication, retry with the browser-cookie fallback (cookies stay
on the Mac and are not written to this repository):

```bash
python3 -m whispertube.youtube \
  'https://www.youtube.com/watch?v=gmj41fQTbfY' \
  --output-dir temp/audio \
  --cookies-from-browser safari
```

Run the unit tests with:

```bash
python3 -m unittest discover -s tests -v
```

Local smoke verification on 2026-09-16 succeeded anonymously with `yt-dlp
2026.08.19`; the test video produced a `.webm` audio file under
`temp/audio-v0-1-converged/` using yt-dlp audio-only format `251`.

## v0.2: local MLX transcription

Install the Apple Silicon-only local inference dependencies:

```bash
python3 -m pip install -r requirements-macos.txt
brew install ffmpeg
```

Transcribe one local audio file with the large-v3 quality target (or choose a
smaller compatible model for a constrained smoke run):

```bash
python3 -m whispertube.transcription \
  /path/to/audio.webm \
  --model mlx-community/whisper-large-v3-mlx \
  --output-dir temp/transcripts
```

The command runs MLX Whisper locally, requests Chinese transcription, converts
the returned text to Taiwan Traditional Chinese with OpenCC, and writes one
UTF-8 Markdown transcript. Model caches, audio, and transcripts remain local
and ignored by Git. CI uses deterministic fakes and does not download models.

On the development Apple Silicon Mac, a 2026-09-16 smoke run used
`mlx-community/whisper-tiny` against the existing v0.1 audio artifact and
completed successfully with recognizable Chinese transcript output.
The run emitted a warning about no JavaScript runtime, but completed without
requiring browser cookies.

## v0.3: end-to-end CLI pipeline

Run both approved local stages with one command:

```bash
python3 -m whispertube.pipeline 'https://www.youtube.com/watch?v=VIDEO_ID' \
  --model mlx-community/whisper-large-v3-mlx \
  --audio-dir temp/pipeline-audio \
  --output-dir temp/pipeline-transcripts
```

The pipeline cleans only audio acquired inside its current temporary directory,
keeps the Markdown transcript, and preserves download, dependency, model,
inference, output, and cleanup error categories.

## v0.4: local graphical UI

Install the pinned local UI dependency in addition to the Apple Silicon
inference dependencies:

```bash
python3 -m pip install -r requirements-ui.txt
python3 -m pip install -r requirements-macos.txt
```

Launch the interface and open its loopback URL in the local browser:

```bash
python3 -m whispertube.gui
```

The UI provides one YouTube URL input, one Transcribe action, visible
running/success/error status, a Markdown preview, and a local Markdown
download. It reuses the v0.3 pipeline and preserves its cause-specific errors.

The server binds explicitly to `127.0.0.1`; public sharing, framework
analytics, monitoring, and direct queue bypass are disabled. Only validated
non-empty UTF-8 Markdown below the configured ignored transcript directory can
be previewed or copied into Gradio's controlled cache for download; the
transcript directory itself is not exposed as an allowed file-serving path. No
public tunnel, hosted processing, telemetry, account, or database is used.

For a constrained local smoke test, select the small model at launch without
changing the normal large-v3 quality target:

```bash
python3 -m whispertube.gui --model mlx-community/whisper-tiny \
  --audio-dir temp/gui-audio-v0-4 --output-dir temp/gui-transcripts-v0-4
```
