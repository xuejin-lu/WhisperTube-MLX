# Local GUI Contract

## Entry point

```text
python3 -m whispertube.gui [--model MODEL]
                              [--audio-dir temp/pipeline-audio]
                              [--output-dir temp/pipeline-transcripts]
                              [--port PORT]
```

The process opens or serves one loopback-only browser interface. It never enables a public share URL.

## Visible controls and outputs

- one labeled YouTube URL textbox;
- one labeled Transcribe button;
- visible status region with idle/running/success/error text;
- Markdown preview region;
- one downloadable Markdown file output.

## Interaction contract

1. Starting clears prior preview/download values and reports `running`.
2. The event accepts only one pending/running submission and invokes `run_pipeline` once.
3. Success reports the transcript filename, full preview, and validated download path.
4. Pipeline errors preserve `<category> error: <actionable message>`.
5. Unexpected exceptions become `application error` without traceback text.
6. Every terminal result restores the Transcribe action.

## Local/privacy contract

- host: `127.0.0.1` only;
- share/tunnel: disabled;
- analytics: disabled;
- monitoring endpoint: disabled;
- direct event API bypass: disabled;
- file access: configured transcript root only, with callback-level path/type/content validation;
- no uploads, credentials, hosted inference, accounts, database, or telemetry.
