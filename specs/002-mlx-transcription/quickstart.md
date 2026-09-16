# Quickstart: Local MLX Transcription

## Local setup

On the maintainer's Apple Silicon Mac:

```bash
python3 -m pip install -r requirements-macos.txt
brew install ffmpeg
```

The first run may download the selected MLX model into the user's local model cache. That model
download is setup data; audio and transcript content remain local to the machine.

## Deterministic tests

```bash
python3 -m unittest discover -s tests -v
```

These tests inject a fake MLX backend and do not download models or audio.

## Local smoke

Use a short local audio fixture and the smaller model when validating the pipeline quickly:

```bash
python3 -m whispertube.transcription \
  "$(find temp/audio-v0-1-converged -maxdepth 1 -type f -name '*.webm' -print -quit)" \
  --model mlx-community/whisper-tiny \
  --output-dir temp/transcripts
```

Record the model, elapsed result, output path, and any human gate in `docs/STATUS.md`; do not record
audio contents or credentials. The expected result is one non-empty UTF-8 Markdown file containing
Chinese text and a successful exit.

## Failure checks

Run deterministic tests for missing input, missing backend, model failure, no text, unsafe output,
unwritable output, and output collision. Each must produce a non-zero result and a cause-specific
message without a success artifact.
