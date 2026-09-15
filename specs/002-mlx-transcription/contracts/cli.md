# CLI Contract: Local MLX Transcription

## Invocation

```text
python3 -m whispertube.transcription INPUT [--output-dir PATH]
                              [--model MODEL_OR_LOCAL_PATH]
                              [--language zh]
                              [--print-command]
```

## Inputs

- `INPUT` identifies exactly one local regular audio file.
- `--output-dir` defaults to `temp/transcripts`; repository-relative paths must remain beneath
  ignored `temp/` or `outputs/` roots. An explicitly provided absolute system-temporary path is
  also allowed when usable; versioned repository paths are never valid runtime destinations.
- `--model` defaults to `mlx-community/whisper-large-v3-mlx` and accepts a local model directory or
  compatible MLX Community reference.
- `--language` defaults to `zh`; v0.2 supports Chinese transcription only.
- `--print-command` is not required because the backend is a Python API; if exposed, it must print
  configuration without loading the model or reading audio.

## Behavior

- Validate input and output before importing or invoking the MLX backend.
- Call the local MLX Whisper adapter with explicit `language="zh"` and `task="transcribe"`.
- Convert returned text locally to Taiwan Traditional Chinese using OpenCC `s2twp`.
- Group transcript text into readable paragraphs targeting roughly 500 Chinese characters each,
  without summarizing or rewriting it.
- Write exactly one UTF-8 Markdown transcript containing minimal source/model metadata and text.
- Do not overwrite an existing transcript unless a future explicit overwrite option is specified.
- Do not upload audio, transcripts, credentials, telemetry, or private runtime artifacts.

## Exit categories

| Category | Meaning |
|---|---|
| 0 | One transcript was written successfully. |
| 2 | CLI arguments, input, or output path are invalid. |
| 3 | MLX Whisper/OpenCC dependency is unavailable. |
| 4 | Model cannot be resolved or loaded. |
| 5 | Local inference failed or returned no text. |
| 6 | Output artifact could not be written or already exists. |

## Privacy contract

The audio path is read locally. Model retrieval, when needed, is a model-cache operation only;
transcription does not send audio or transcript content to a hosted service. Runtime artifacts and
model caches remain ignored and local.
