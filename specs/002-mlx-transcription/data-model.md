# Data Model: Local MLX Transcription

## LocalAudioInput

- `path`: user-provided local file path.
- `resolved_path`: validated path used for reading; must remain local.
- `readable`: whether the path is a regular readable file.
- `format`: inferred by the local audio decoder; no new media conversion is performed by v0.2.

## WhisperModelSource

- `reference`: default `mlx-community/whisper-large-v3-mlx`, an explicit local model directory, or
  another compatible MLX Community reference selected by the maintainer.
- `is_default`: whether the quality-target default was used.
- `cache_location`: local model cache location, never a versioned repository path.

## TranscriptionRequest

- `input`: exactly one `LocalAudioInput`.
- `model`: one `WhisperModelSource`.
- `language`: `zh` for Chinese recognition.
- `task`: `transcribe`, never implicit translation.
- `output_dir`: ignored local runtime directory.
- `output_path`: one derived Markdown artifact path; existing artifacts are not overwritten by default.

## TranscriptArtifact

- `source_name`: source filename recorded in the Markdown header.
- `model_reference`: model identifier recorded in the Markdown header.
- `language`: requested language.
- `text`: non-empty UTF-8 Taiwan Traditional Chinese transcript text grouped into readable
  paragraphs targeting roughly 500 Chinese characters per paragraph.
- `path`: ignored local Markdown output path.

## Failure categories

- `input`: missing, non-file, unreadable, or unsupported audio input.
- `dependency`: MLX Whisper or OpenCC unavailable.
- `model`: model cannot be resolved or loaded.
- `inference`: backend returns an error or no transcript text.
- `output`: unsafe, unwritable, colliding, or otherwise unusable output path.
