# Quickstart: Local YouTube Audio Acquisition

Run these commands from the repository root.

## Deterministic validation

```bash
python3 -m unittest discover -s tests -v
```

Expected result: all URL and command-construction tests pass without network access or browser
credentials.

## Inspect the normalized command without downloading

```bash
python3 -m whispertube.youtube \
  'https://www.youtube.com/watch?v=gmj41fQTbfY&list=PL123&index=2' \
  --output-dir temp/audio \
  --print-command
```

Expected result: the printed command contains `--no-playlist` and the canonical URL ending in
`watch?v=gmj41fQTbfY`, with no playlist parameters.

## Anonymous local smoke test

Install the local downloader if needed, then run:

```bash
python3 -m pip install -U yt-dlp
python3 -m whispertube.youtube \
  'https://www.youtube.com/watch?v=gmj41fQTbfY' \
  --output-dir temp/audio
```

Expected result: yt-dlp reports `[download] 100%` and an audio file exists under `temp/audio/`.
The directory is ignored by Git and no cookie file is created in the repository.

## Local browser-session retry

If anonymous access is blocked, retry without exporting cookies:

```bash
python3 -m whispertube.youtube \
  'https://www.youtube.com/watch?v=gmj41fQTbfY' \
  --output-dir temp/audio \
  --cookies-from-browser safari
```

If macOS requests Keychain or browser permission, that is the only human authorization gate. If
the browser session is unavailable, record the downloader's error and leave the repository free of
credential material.
