import tempfile
import sys
import types
import unittest
from contextlib import redirect_stderr
from io import StringIO
from pathlib import Path
from unittest.mock import Mock, patch

from whispertube.transcription import (
    DEFAULT_MODEL,
    DependencyError,
    InferenceError,
    InputError,
    ModelError,
    OutputError,
    _load_converter,
    format_paragraphs,
    main,
    transcribe_audio,
)


class TranscriptionTests(unittest.TestCase):
    def test_writes_one_utf8_traditional_markdown_artifact(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            source = Path(temp_dir) / "lecture.m4a"
            source.write_bytes(b"local audio fixture")
            backend = Mock(return_value={"text": "电脑结构和历史"})
            converter = Mock(return_value="電腦結構和歷史")

            output = transcribe_audio(
                source,
                output_dir=Path(temp_dir) / "transcripts",
                transcriber=backend,
                converter=converter,
            )

            self.assertEqual(output.name, "lecture.md")
            self.assertEqual(output.read_text(encoding="utf-8").count("## Transcript"), 1)
            self.assertIn("電腦結構和歷史", output.read_text(encoding="utf-8"))
            self.assertIn("lecture.m4a", output.read_text(encoding="utf-8"))
            converter.assert_called_once_with("电脑结构和历史")

    def test_formats_transcript_into_readable_paragraphs_without_rewriting(self) -> None:
        text = "甲" * 501 + "乙"

        formatted = format_paragraphs(text)

        paragraphs = formatted.split("\n\n")
        self.assertEqual(len(paragraphs), 2)
        self.assertTrue(all(len(paragraph) <= 500 for paragraph in paragraphs))
        self.assertEqual("".join(paragraphs), text)

    def test_prefers_sentence_boundary_near_paragraph_target(self) -> None:
        text = "甲" * 480 + "。" + "乙" * 119

        formatted = format_paragraphs(text)

        paragraphs = formatted.split("\n\n")
        self.assertEqual(len(paragraphs), 2)
        self.assertTrue(paragraphs[0].endswith("。"))
        self.assertEqual("".join(paragraphs), text)

    def test_hard_splits_pathological_span_without_losing_content(self) -> None:
        text = "甲" * 1001

        formatted = format_paragraphs(text)

        paragraphs = formatted.split("\n\n")
        self.assertEqual([len(paragraph) for paragraph in paragraphs], [500, 500, 1])
        self.assertEqual("".join(paragraphs), text)

    def test_uses_local_input_and_explicit_chinese_transcription(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            source = Path(temp_dir) / "lecture.webm"
            source.write_bytes(b"local audio fixture")
            backend = Mock(return_value={"text": "你好"})

            transcribe_audio(
                source,
                output_dir=Path(temp_dir) / "transcripts",
                model="local-model",
                transcriber=backend,
                converter=lambda text: text,
            )

            backend.assert_called_once_with(
                str(source),
                path_or_hf_repo="local-model",
                language="zh",
                task="transcribe",
                verbose=False,
            )

    def test_default_model_targets_large_v3(self) -> None:
        self.assertEqual(DEFAULT_MODEL, "mlx-community/whisper-large-v3-mlx")

    def test_invalid_input_fails_before_backend(self) -> None:
        backend = Mock()
        with self.assertRaises(InputError):
            transcribe_audio(
                Path("does-not-exist.webm"),
                transcriber=backend,
                converter=lambda text: text,
            )
        backend.assert_not_called()

    def test_non_file_and_unsupported_inputs_fail_before_backend(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            directory = Path(temp_dir) / "audio"
            directory.mkdir()
            unsupported = Path(temp_dir) / "notes.txt"
            unsupported.write_text("not audio", encoding="utf-8")
            for source in (directory, unsupported):
                backend = Mock()
                with self.assertRaises(InputError):
                    transcribe_audio(
                        source,
                        transcriber=backend,
                        converter=lambda text: text,
                    )
                backend.assert_not_called()

    def test_unreadable_input_fails_before_backend(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            source = Path(temp_dir) / "lecture.wav"
            source.write_bytes(b"local audio fixture")
            backend = Mock()
            with patch("whispertube.transcription.os.access", return_value=False):
                with self.assertRaises(InputError):
                    transcribe_audio(
                        source,
                        transcriber=backend,
                        converter=lambda text: text,
                    )
            backend.assert_not_called()

    def test_unsafe_output_path_fails_before_backend(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            source = Path(temp_dir) / "lecture.wav"
            source.write_bytes(b"local audio fixture")
            backend = Mock()
            with self.assertRaises(OutputError):
                transcribe_audio(
                    source,
                    output_dir="temp/../../outside",
                    transcriber=backend,
                    converter=lambda text: text,
                )
            backend.assert_not_called()

    def test_existing_output_is_not_overwritten(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            source = Path(temp_dir) / "lecture.wav"
            source.write_bytes(b"local audio fixture")
            output_dir = Path(temp_dir) / "transcripts"
            output_dir.mkdir()
            output = output_dir / "lecture.md"
            output.write_text("keep this", encoding="utf-8")
            backend = Mock()

            with self.assertRaises(OutputError):
                transcribe_audio(
                    source,
                    output_dir=output_dir,
                    transcriber=backend,
                    converter=lambda text: text,
                )

            self.assertEqual(output.read_text(encoding="utf-8"), "keep this")
            backend.assert_not_called()

    def test_unwritable_output_directory_fails_before_backend(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            source = Path(temp_dir) / "lecture.wav"
            source.write_bytes(b"local audio fixture")
            output_target = Path(temp_dir) / "not-a-directory"
            output_target.write_text("occupied", encoding="utf-8")
            backend = Mock()

            with self.assertRaises(OutputError):
                transcribe_audio(
                    source,
                    output_dir=output_target,
                    transcriber=backend,
                    converter=lambda text: text,
                )

            backend.assert_not_called()

    def test_missing_backend_is_actionable(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            source = Path(temp_dir) / "lecture.wav"
            source.write_bytes(b"local audio fixture")
            with patch(
                "whispertube.transcription._load_transcriber",
                side_effect=DependencyError("mlx-whisper is not installed"),
            ):
                with self.assertRaises(DependencyError):
                    transcribe_audio(source, output_dir=Path(temp_dir) / "transcripts")

    def test_model_load_failure_is_distinct(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            source = Path(temp_dir) / "lecture.wav"
            source.write_bytes(b"local audio fixture")
            backend = Mock(side_effect=FileNotFoundError("model missing"))
            with self.assertRaises(ModelError):
                transcribe_audio(
                    source,
                    output_dir=Path(temp_dir) / "transcripts",
                    transcriber=backend,
                    converter=lambda text: text,
                )

    def test_missing_ffmpeg_is_a_dependency_failure_before_backend(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            source = Path(temp_dir) / "lecture.wav"
            source.write_bytes(b"local audio fixture")
            backend = Mock()
            with patch("whispertube.transcription.shutil.which", return_value=None):
                with self.assertRaises(DependencyError):
                    transcribe_audio(
                        source,
                        output_dir=Path(temp_dir) / "transcripts",
                        transcriber=None,
                        converter=lambda text: text,
                    )
            backend.assert_not_called()

    def test_audio_decode_value_error_is_not_mislabeled_as_model_failure(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            source = Path(temp_dir) / "lecture.wav"
            source.write_bytes(b"local audio fixture")
            with self.assertRaises(InferenceError):
                transcribe_audio(
                    source,
                    output_dir=Path(temp_dir) / "transcripts",
                    transcriber=Mock(side_effect=ValueError("audio decode failed")),
                    converter=lambda text: text,
                )

    def test_backend_missing_ffmpeg_is_a_dependency_failure(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            source = Path(temp_dir) / "lecture.wav"
            source.write_bytes(b"local audio fixture")
            with self.assertRaises(DependencyError):
                transcribe_audio(
                    source,
                    output_dir=Path(temp_dir) / "transcripts",
                    transcriber=Mock(side_effect=FileNotFoundError("ffmpeg executable not found")),
                    converter=lambda text: text,
                )

    def test_opencc_adapter_uses_s2tw(self) -> None:
        factory = Mock(return_value=Mock(convert=lambda text: text))
        fake_opencc = types.SimpleNamespace(OpenCC=factory)
        with patch.dict(sys.modules, {"opencc": fake_opencc}):
            _load_converter()

        factory.assert_called_once_with("s2tw")

    def test_inference_failure_and_empty_text_are_distinct_from_input(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            source = Path(temp_dir) / "lecture.wav"
            source.write_bytes(b"local audio fixture")
            with self.assertRaises(InferenceError):
                transcribe_audio(
                    source,
                    output_dir=Path(temp_dir) / "runtime-error",
                    transcriber=Mock(side_effect=RuntimeError("decode failed")),
                    converter=lambda text: text,
                )
            with self.assertRaises(InferenceError):
                transcribe_audio(
                    source,
                    output_dir=Path(temp_dir) / "empty-result",
                    transcriber=Mock(return_value={"text": "  "}),
                    converter=lambda text: text,
                )

    def test_cli_reports_input_failure_with_exit_code(self) -> None:
        error = StringIO()
        with redirect_stderr(error):
            result = main(["missing.wav"])
        self.assertEqual(result, InputError.exit_code)
        self.assertIn("input error", error.getvalue())

    def test_cli_reports_dependency_failure_with_exit_code(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            source = Path(temp_dir) / "lecture.wav"
            source.write_bytes(b"local audio fixture")
            error = StringIO()
            with patch(
                "whispertube.transcription._load_transcriber",
                side_effect=DependencyError("mlx-whisper is not installed"),
            ), redirect_stderr(error):
                result = main([str(source), "--output-dir", str(Path(temp_dir) / "transcripts")])
        self.assertEqual(result, DependencyError.exit_code)
        self.assertIn("dependency error", error.getvalue())


if __name__ == "__main__":
    unittest.main()
