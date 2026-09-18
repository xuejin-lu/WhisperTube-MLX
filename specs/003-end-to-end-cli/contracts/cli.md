# CLI Contract: End-to-End Pipeline

```text
python3 -m whispertube.pipeline URL [--audio-dir temp/pipeline-audio]
                                  [--output-dir temp/transcripts] [--model MODEL]
                                  [--cookies-from-browser BROWSER] [--yt-dlp PATH]
```

One URL prints one transcript path. Current-run audio is removed after either transcription result;
output/model options pass unchanged. Download errors use exit 2, transcription retains exits 2–6,
and cleanup after successful transcription uses exit 7. If cleanup fails while a stage error is
already active, the original stage category and exit code are retained and stderr also warns that
cleanup failed and current-run audio may remain. Acquisition failure removes only partial artifacts
inside the default acquirer's dedicated `run-*` directory. No audio, transcript, or credential uploads.
