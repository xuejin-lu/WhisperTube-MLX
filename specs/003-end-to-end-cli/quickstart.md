# Quickstart: End-to-End CLI Pipeline

```bash
python3 -m unittest tests.test_pipeline -v
python3 -m unittest discover -s tests -v
python3 -m whispertube.pipeline 'https://www.youtube.com/watch?v=gmj41fQTbfY' \
  --model mlx-community/whisper-tiny --audio-dir temp/pipeline-audio \
  --output-dir temp/pipeline-transcripts
```

Expect one local Markdown path and no current-run audio remaining under `temp/pipeline-audio/`.
