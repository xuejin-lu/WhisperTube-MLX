# CLI Contract: Local YouTube Audio Acquisition

## Invocation

```text
python3 -m whispertube.youtube URL [--output-dir PATH]
                            [--cookies-from-browser BROWSER]
                            [--yt-dlp EXECUTABLE]
                            [--print-command]
```

## Inputs

- `URL` is one supported YouTube watch, `youtu.be`, or Shorts URL.
- `--output-dir` selects a local runtime directory and defaults to `temp/audio`.
- `--cookies-from-browser BROWSER` is optional and is intended for an explicit retry after
  anonymous access is blocked. The value is passed to the local downloader; it is never exported.
- `--yt-dlp EXECUTABLE` overrides the executable name for testing or a non-default installation.
- `--print-command` prints the shell-escaped equivalent command and does not invoke the downloader.

## Behavior

- The URL is validated and normalized before the downloader is started.
- Playlist parameters are discarded from the canonical URL.
- The downloader receives `--no-playlist`, `--format bestaudio/best`, and an output template of
  `PATH/%(title)s [%(id)s].%(ext)s`.
- The output directory is created when a real download is requested.
- If the output directory cannot be created or written, the CLI reports an actionable output error
  and does not invoke the downloader.
- Downloader stdout and stderr remain visible to the local user.

## Exit codes

| Code | Meaning |
|---:|---|
| 0 | Command printed successfully or download completed successfully. |
| 2 | Invalid CLI arguments or invalid/unsupported YouTube URL. |
| 127 | The configured downloader executable could not be found. |
| other non-zero | The downloader returned an acquisition failure. |

An unavailable output directory is a non-success result and must be distinguishable from a
downloader failure in the user-facing error message.

## Privacy contract

The CLI never accepts or creates a repository cookie export. Browser authentication is supplied
only through the downloader's local browser integration, and runtime media is written under an
ignored local path.
