# Quickstart: Local Graphical UI

## Install

```bash
python3 -m pip install -r requirements-ui.txt
python3 -m pip install -r requirements-macos.txt
brew install ffmpeg yt-dlp
```

## Deterministic validation

```bash
python3 -m unittest tests.test_gui -v
python3 -m unittest discover -s tests -v
python3 -m compileall -q whispertube tests
git diff --check
```

## Local launch

```bash
python3 -m whispertube.gui
```

Expect a loopback URL only, no public share URL, one URL input, one Transcribe action, visible status,
Markdown preview, and a download output.

## Apple Silicon smoke

```bash
python3 -m whispertube.gui --model mlx-community/whisper-tiny \
  --audio-dir temp/gui-audio-v0-4 --output-dir temp/gui-transcripts-v0-4
```

In the opened local browser, submit `https://www.youtube.com/watch?v=gmj41fQTbfY`. Expect a non-empty
Markdown preview/download, retained transcript, empty audio directory, and no credentials or public URL.
