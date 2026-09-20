# Troubleshooting

## Setup fails

WhisperTube supports native Python 3.10 or newer on Apple Silicon macOS. Run:

```bash
./scripts/setup_macos.sh
```

The script creates or reuses `.venv` and installs only the pinned yt-dlp package.
It does not remove downloads, cookies, browser profiles, or caches. If an
existing environment is incomplete, repair only that disposable `.venv` after
confirming it contains no user data.

## `yt-dlp` is missing

The launcher prepends `.venv/bin` to `PATH`. Rerun setup and check that this file
exists:

```bash
test -x .venv/bin/yt-dlp
```

Do not rely on a global yt-dlp installation for the normal workflow.

## Invalid URL or unexpected download failure

Use one explicit video URL or one explicit `/playlist?list=...` URL. A watch URL
that contains `list=` is intentionally treated as one video. The command returns
a non-zero status for invalid input, missing dependencies, unwritable output, or
unexpected yt-dlp failure; read the terminal error and correct that condition
before retrying.

## YouTube authentication

Anonymous download is the default. If YouTube requires local browser access, opt
in explicitly:

```bash
./scripts/launch_macos.sh \
  --cookies-from-browser safari \
  'https://www.youtube.com/watch?v=VIDEO_ID'
```

Cookies remain local and are never exported to the repository or uploaded to
Colab. Browser login, Keychain, or privacy prompts are user-owned decisions;
WhisperTube does not capture credentials or bypass prompts.

## Output and cleanup

Normal output is `~/Downloads/WhisperTube/`. Use an absolute temporary output root
for smoke tests. Setup and launch never delete user downloads or caches. To remove
the project environment, stop any command and remove only the disposable `.venv`
after reviewing its contents.

## What this product does not do

The current mainline does not transcribe, run MLX/Whisper/OpenCC/Gradio, start a
localhost server, upload to Colab, or convert audio to MP3. The former local
transcription workflow is preserved only in the historical v1.0.0 release and Git
history.
