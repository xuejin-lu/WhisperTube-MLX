# Research: Local MLX Transcription

## Decision 1: Use the maintained `mlx-whisper` implementation

- **Decision**: Use the `mlx-whisper` package from the Apple MLX examples ecosystem as the local
  inference adapter, imported lazily by the application.
- **Rationale**: The current package exposes a small Python API, accepts a local audio path, and
  accepts either a local MLX model directory or a Hugging Face MLX Community model reference. This
  preserves a testable application boundary while keeping model loading out of CI.
- **Evidence**: The [official MLX Whisper README](https://github.com/ml-explore/mlx-examples/tree/main/whisper)
  documents `pip install mlx-whisper` and `mlx_whisper.transcribe(...)`; the current PyPI metadata
  describes the same API and local/Hugging Face model resolution.
- **Version observation**: PyPI reported `mlx-whisper` 0.4.3 during this planning run. The local
  dependency file will pin the researched version for reproducible maintainer setup, with an
  explicit upgrade task when the API is intentionally revisited.
- **Alternatives considered**: Hosted transcription APIs violate the constitution. Generic CPU
  Whisper implementations do not satisfy the Apple Silicon MLX target. Directly vendoring the
  upstream implementation would create unnecessary maintenance scope.

## Decision 2: Target `whisper-large-v3-mlx`, allow an explicit smaller smoke model

- **Decision**: Use `mlx-community/whisper-large-v3-mlx` as the default quality target and permit an
  explicit smaller compatible model for constrained local smoke runs.
- **Rationale**: The MLX Community model is a verified MLX-format Whisper large-v3 checkpoint. Its
  observed size is about 3.08 GB, so deterministic CI and short validation runs must not require
  it. The implementation must keep model choice configurable without silently downgrading the
  default.
- **Evidence**: The [MLX Community large-v3 model page](https://huggingface.co/mlx-community/whisper-large-v3-mlx)
  identifies it as an automatic speech recognition MLX model and lists the checkpoint size. The
  upstream CLI also demonstrates model selection and a tiny default for lightweight examples.
- **Alternatives considered**: Defaulting to tiny would make the quality target implicit and weaken
  the milestone. Requiring large-v3 in CI would violate deterministic and hardware-independent CI.

## Decision 3: Convert transcript text locally to Taiwan Traditional Chinese

- **Decision**: Pass `language="zh"` and `task="transcribe"` to the MLX Whisper API, then apply the
  deterministic OpenCC `s2twp` conversion to the returned text before Markdown output.
- **Rationale**: `transcribe` preserves speech recognition semantics rather than translation, while
  OpenCC provides offline dictionary-based Simplified-to-Taiwan-Traditional conversion aligned with
  the constitution's output path.
- **Evidence**: The [official OpenCC project](https://github.com/BYVoid/OpenCC) documents local,
  dictionary-based conversion and the Python `opencc.OpenCC(...).convert(...)` API. The MLX Whisper
  source documents explicit `language` and `task` decoding options.
- **Alternatives considered**: An ad-hoc character map cannot handle phrase-level regional wording.
  Asking the model for translation would change the requested transcription semantics.

## Decision 4: Keep CI deterministic with an injected backend

- **Decision**: Put all real MLX imports behind an adapter and inject a fake transcriber/converter in
  unit tests. Reserve real model execution for a local Apple Silicon smoke test.
- **Rationale**: CI cannot depend on Apple Silicon, model downloads, network access, or private audio.
  Injection also makes input/output/error behavior independently testable.
- **Alternatives considered**: Mocking at arbitrary module-global call sites would make the design
  less explicit and couple tests to import order. Running a live model in CI would be slow and
  nondeterministic.

## Open questions resolved

No unresolved product questions remain for the v0.2 scope. Model quality benchmarking, timestamps,
diarization, summarization, and YouTube-to-transcription composition remain later work.
