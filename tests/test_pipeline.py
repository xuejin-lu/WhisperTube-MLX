import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout
from io import StringIO
from pathlib import Path
from unittest.mock import Mock, patch

from whispertube.pipeline import CleanupError, DownloadError, main, run_pipeline
from whispertube.transcription import ModelError, OutputError


class PipelineTests(unittest.TestCase):
    def test_composes_stages_and_propagates_options(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            audio = root / "audio" / "video.webm"
            audio.parent.mkdir()
            audio.write_bytes(b"audio")
            transcript = root / "transcripts" / "video.md"
            acquire = Mock(return_value=audio)
            transcribe = Mock(return_value=transcript)

            result = run_pipeline(
                "https://youtu.be/gmj41fQTbfY?list=ignored",
                audio_dir=audio.parent,
                output_dir=transcript.parent,
                model="tiny-model",
                cookies_from_browser="safari",
                yt_dlp="custom-yt-dlp",
                acquire=acquire,
                transcribe=transcribe,
            )

            self.assertEqual(result, transcript)
            acquire.assert_called_once_with(
                "https://youtu.be/gmj41fQTbfY?list=ignored",
                audio_dir=audio.parent,
                cookies_from_browser="safari",
                yt_dlp="custom-yt-dlp",
            )
            transcribe.assert_called_once_with(audio, output_dir=transcript.parent, model="tiny-model")
            self.assertFalse(audio.exists())

    def test_cleans_audio_after_transcription_failure(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            audio = Path(temp_dir) / "audio" / "video.webm"
            audio.parent.mkdir()
            audio.write_bytes(b"audio")
            with self.assertRaises(ModelError):
                run_pipeline(
                    "https://youtu.be/gmj41fQTbfY",
                    audio_dir=audio.parent,
                    acquire=Mock(return_value=audio),
                    transcribe=Mock(side_effect=ModelError("missing model")),
                )
            self.assertFalse(audio.exists())

    def test_rejects_acquired_path_outside_owned_root_without_deleting_it(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            outside = root / "keep.webm"
            outside.write_bytes(b"keep")
            with self.assertRaises(DownloadError):
                run_pipeline(
                    "https://youtu.be/gmj41fQTbfY",
                    audio_dir=root / "owned",
                    acquire=Mock(return_value=outside),
                    transcribe=Mock(),
                )
            self.assertTrue(outside.exists())

    def test_missing_audio_at_cleanup_is_already_clean(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            audio = Path(temp_dir) / "audio" / "video.webm"
            audio.parent.mkdir()
            audio.write_bytes(b"audio")
            transcript = Path(temp_dir) / "video.md"

            def transcribe_then_remove(path, **kwargs):
                path.unlink()
                return transcript

            self.assertEqual(
                run_pipeline(
                    "https://youtu.be/gmj41fQTbfY",
                    audio_dir=audio.parent,
                    acquire=Mock(return_value=audio),
                    transcribe=transcribe_then_remove,
                ),
                transcript,
            )

    def test_cleanup_failure_after_success_is_distinct(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            audio = Path(temp_dir) / "audio" / "video.webm"
            audio.parent.mkdir()
            audio.write_bytes(b"audio")
            with patch("pathlib.Path.unlink", side_effect=PermissionError("denied")):
                with self.assertRaises(CleanupError):
                    run_pipeline(
                        "https://youtu.be/gmj41fQTbfY",
                        audio_dir=audio.parent,
                        acquire=Mock(return_value=audio),
                        transcribe=Mock(return_value=Path(temp_dir) / "video.md"),
                    )

    def test_cleanup_failure_preserves_transcription_category_and_reports_residual_audio(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            audio = Path(temp_dir) / "audio" / "video.webm"
            audio.parent.mkdir()
            audio.write_bytes(b"audio")
            with patch("pathlib.Path.unlink", side_effect=PermissionError("denied")):
                with self.assertRaises(ModelError) as caught:
                    run_pipeline(
                        "https://youtu.be/gmj41fQTbfY",
                        audio_dir=audio.parent,
                        acquire=Mock(return_value=audio),
                        transcribe=Mock(side_effect=ModelError("missing model")),
                    )

            self.assertEqual(caught.exception.category, "model")
            self.assertEqual(caught.exception.exit_code, ModelError.exit_code)
            self.assertIn("cleanup failed", str(caught.exception))
            self.assertIn("current-run audio may remain", str(caught.exception))
            self.assertTrue(audio.exists())

    def test_default_acquirer_removes_partial_run_directory_after_failure(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            audio_root = Path(temp_dir) / "audio"
            transcribe = Mock()

            def fail_after_partial_download(argv):
                run_dir = Path(argv[argv.index("--output-dir") + 1])
                (run_dir / "partial.webm").write_bytes(b"partial")
                return 1

            with patch("whispertube.pipeline.youtube.main", side_effect=fail_after_partial_download):
                with self.assertRaises(DownloadError):
                    run_pipeline(
                        "https://youtu.be/gmj41fQTbfY",
                        audio_dir=audio_root,
                        transcribe=transcribe,
                    )

            transcribe.assert_not_called()
            self.assertEqual(list(audio_root.iterdir()), [])

    def test_download_failure_does_not_call_transcription(self) -> None:
        transcribe = Mock()
        with self.assertRaises(DownloadError):
            run_pipeline(
                "https://youtu.be/gmj41fQTbfY",
                acquire=Mock(side_effect=DownloadError("download failed")),
                transcribe=transcribe,
            )
        transcribe.assert_not_called()

    def test_transcription_output_error_is_preserved(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            audio = Path(temp_dir) / "audio" / "video.webm"
            audio.parent.mkdir()
            audio.write_bytes(b"audio")
            with self.assertRaises(OutputError):
                run_pipeline(
                    "https://youtu.be/gmj41fQTbfY",
                    audio_dir=audio.parent,
                    acquire=Mock(return_value=audio),
                    transcribe=Mock(side_effect=OutputError("collision")),
                )

    def test_cli_prints_success_and_reports_stage_error(self) -> None:
        output = StringIO()
        with patch("whispertube.pipeline.run_pipeline", return_value=Path("temp/out.md")), redirect_stdout(output):
            self.assertEqual(main(["https://youtu.be/gmj41fQTbfY"]), 0)
        self.assertIn("temp/out.md", output.getvalue())

        error = StringIO()
        with patch("whispertube.pipeline.run_pipeline", side_effect=DownloadError("failed")), redirect_stderr(error):
            self.assertEqual(main(["https://youtu.be/gmj41fQTbfY"]), DownloadError.exit_code)
        self.assertIn("download error", error.getvalue())


if __name__ == "__main__":
    unittest.main()
