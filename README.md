# WhisperTube-MLX
Local YouTube transcription app powered by MLX Whisper for Apple Silicon.

## v0.1: local audio acquisition

The first milestone provides a small Python CLI that normalizes one YouTube URL
and downloads that video's best available audio-only representation (`bestaudio`)
with local `yt-dlp`. Playlist parameters are ignored; only the current video is
downloaded.

Install `yt-dlp` on the maintainer's Mac, then run this local verification
command from the repository root:

```bash
python3 -m pip install -U yt-dlp
python3 -m whispertube.youtube \
  'https://www.youtube.com/watch?v=gmj41fQTbfY' \
  --output-dir temp/audio
```

The expected evidence is a `[download] 100%` line and an audio file under
`temp/audio/`. The directory is ignored by Git. If YouTube requires local
browser authentication, retry with the browser-cookie fallback (cookies stay
on the Mac and are not written to this repository):

```bash
python3 -m whispertube.youtube \
  'https://www.youtube.com/watch?v=gmj41fQTbfY' \
  --output-dir temp/audio \
  --cookies-from-browser safari
```

Run the unit tests with:

```bash
python3 -m unittest discover -s tests -v
```

Local smoke verification on 2026-09-16 succeeded anonymously with `yt-dlp
2026.08.19`; the test video produced a `.webm` audio file under
`temp/audio-v0-1-converged/` using yt-dlp audio-only format `251`.
The run emitted a warning about no JavaScript runtime, but completed without
requiring browser cookies.
