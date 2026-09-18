# CLI Contract: End-to-End Pipeline

```text
python3 -m whispertube.pipeline URL [--audio-dir temp/pipeline-audio]
                                  [--output-dir temp/transcripts] [--model MODEL]
                                  [--cookies-from-browser BROWSER] [--yt-dlp PATH]
```

One URL prints one transcript path. Current-run audio is removed after either transcription result;
output/model options pass unchanged. Download errors use exit 2, transcription retains exits 2–6,
and cleanup after successful transcription uses exit 7. No audio, transcript, or credential uploads.
