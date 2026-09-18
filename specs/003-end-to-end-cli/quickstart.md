# Quickstart: End-to-End CLI Pipeline

```bash
python3 -m unittest tests.test_pipeline -v
python3 -m unittest discover -s tests -v
python3 -m whispertube.pipeline 'https://www.youtube.com/watch?v=gmj41fQTbfY' \
  --model mlx-community/whisper-tiny --audio-dir temp/pipeline-audio \
  --output-dir temp/pipeline-transcripts
```

Expect one local Markdown path and no current-run audio remaining under `temp/pipeline-audio/`.
Acquisition failure also removes its dedicated `run-*` directory. If cleanup itself fails, the CLI
retains the original stage category and exit code while warning that current-run audio may remain.
