import tempfile
import unittest
from pathlib import Path
from unittest.mock import Mock, patch

from whispertube.gui import begin_run, build_app, execute_pipeline_request, launch_app, run_gui_request
from whispertube.pipeline import CleanupError, DownloadError
from whispertube.transcription import DependencyError, InferenceError, ModelError, OutputError

class GUITests(unittest.TestCase):
    def test_begin_run_clears_stale_result_and_disables_action(self) -> None:
        result = begin_run()

        self.assertEqual(result.status.value, "running")
        self.assertIn("running", result.message.lower())
        self.assertEqual(result.preview, "")
        self.assertIsNone(result.transcript_path)
        self.assertFalse(result.action_enabled)

    def test_blank_url_is_rejected_without_pipeline_call(self) -> None:
        pipeline = Mock()

        with self.assertRaisesRegex(ValueError, "YouTube URL is required"):
            execute_pipeline_request("  \n ", pipeline=pipeline)

        pipeline.assert_not_called()

    def test_valid_request_trims_url_and_propagates_launch_configuration(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            transcript = root / "transcripts" / "result.md"
            pipeline = Mock(return_value=transcript)

            result = execute_pipeline_request(
                "  https://youtu.be/gmj41fQTbfY  ",
                model="tiny-model",
                audio_dir=root / "audio",
                output_dir=transcript.parent,
                pipeline=pipeline,
            )

            self.assertEqual(result, transcript)
            pipeline.assert_called_once_with(
                "https://youtu.be/gmj41fQTbfY",
                model="tiny-model",
                audio_dir=root / "audio",
                output_dir=transcript.parent,
            )

    def test_build_app_has_labeled_components_and_single_private_event(self) -> None:
        app = build_app(handler=Mock(return_value=("Success", "# Transcript", "result.md", True)))
        self.addCleanup(app.close)
        config = app.get_config_file()
        components = config["components"]

        component_types = {component["type"] for component in components}
        self.assertTrue({"textbox", "button", "markdown", "file"}.issubset(component_types))
        labels = {component["props"].get("label") for component in components}
        self.assertIn("YouTube URL", labels)
        self.assertIn("Status", labels)
        self.assertIn("Transcript preview", labels)
        self.assertIn("Download Markdown", labels)

        terminal_events = [
            dependency
            for dependency in config["dependencies"]
            if dependency.get("trigger_mode") == "once" and dependency.get("queue") is True
        ]
        self.assertEqual(len(terminal_events), 1)
        self.assertEqual(terminal_events[0]["api_visibility"], "private")
        self.assertEqual(app._queue.default_concurrency_limit, 1)
        self.assertFalse(app.api_open)

    def test_success_and_approved_failures_have_safe_terminal_state(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            transcript = root / "result.md"
            transcript.write_text("# Transcript\n", encoding="utf-8")
            success = run_gui_request("https://youtu.be/gmj41fQTbfY", output_dir=root, pipeline=Mock(return_value=transcript))
            self.assertEqual(success.status.value, "success")
            self.assertIn("result.md", success.message)
            self.assertTrue(success.action_enabled)

            failures = [
                DownloadError("blocked"),
                DependencyError("missing ffmpeg"),
                ModelError("missing model"),
                InferenceError("decode failed"),
                OutputError("collision"),
                CleanupError("audio may remain"),
            ]
            for failure in failures:
                with self.subTest(category=failure.category):
                    result = run_gui_request(
                        "https://youtu.be/gmj41fQTbfY",
                        output_dir=root,
                        pipeline=Mock(side_effect=failure),
                    )
                    self.assertEqual(result.status.value, "error")
                    self.assertIn(f"{failure.category} error", result.message)
                    self.assertIn(str(failure), result.message)
                    self.assertEqual(result.preview, "")
                    self.assertIsNone(result.transcript_path)
                    self.assertTrue(result.action_enabled)

    def test_unexpected_failure_hides_traceback_and_sensitive_details(self) -> None:
        result = run_gui_request(
            "https://youtu.be/gmj41fQTbfY",
            pipeline=Mock(side_effect=RuntimeError("secret /Users/example/cookies.txt")),
        )

        self.assertEqual(result.status.value, "error")
        self.assertEqual(result.message, "application error: unexpected local failure")
        self.assertNotIn("Traceback", result.message)
        self.assertNotIn("cookies", result.message)

    def test_launch_is_explicitly_local_private_and_non_telemetric(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            output_root = Path(temp_dir) / "transcripts"
            app = Mock()

            launch_app(app, output_dir=output_root, port=9876, inbrowser=False)

            app.launch.assert_called_once_with(
                server_name="127.0.0.1",
                server_port=9876,
                share=False,
                inbrowser=False,
                show_error=False,
                enable_monitoring=False,
                strict_cors=True,
                allowed_paths=[str(output_root.resolve())],
                footer_links=[],
            )

        built = build_app(handler=Mock(return_value=("", "", None, True)))
        self.addCleanup(built.close)
        self.assertFalse(built.analytics_enabled)

    def test_launch_rejects_unapproved_file_serving_root(self) -> None:
        app = Mock()

        with self.assertRaisesRegex(ValueError, "transcript directory"):
            launch_app(app, output_dir=Path.cwd() / "private-transcripts", inbrowser=False)

        app.launch.assert_not_called()

    def test_valid_markdown_preview_and_download_match_artifact_bytes(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir) / "transcripts"
            root.mkdir()
            transcript = root / "result.md"
            content = "# Transcript\n\n台灣繁體中文\n"
            transcript.write_text(content, encoding="utf-8")

            result = run_gui_request(
                "https://youtu.be/gmj41fQTbfY",
                output_dir=root,
                pipeline=Mock(return_value=transcript),
            )

            self.assertEqual(result.status.value, "success")
            self.assertEqual(result.preview, content)
            self.assertEqual(result.preview.encode("utf-8"), transcript.read_bytes())
            self.assertEqual(result.transcript_path, transcript.resolve())

    def test_unsafe_or_invalid_transcript_results_are_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            base = Path(temp_dir)
            root = base / "transcripts"
            root.mkdir()
            outside = base / "outside.md"
            outside.write_text("# Keep", encoding="utf-8")
            missing = root / "missing.md"
            empty = root / "empty.md"
            empty.touch()
            wrong_suffix = root / "result.txt"
            wrong_suffix.write_text("text", encoding="utf-8")
            invalid_utf8 = root / "invalid.md"
            invalid_utf8.write_bytes(b"\xff\xfe")

            for path in [outside, missing, empty, wrong_suffix, invalid_utf8]:
                with self.subTest(path=path.name):
                    result = run_gui_request(
                        "https://youtu.be/gmj41fQTbfY",
                        output_dir=root,
                        pipeline=Mock(return_value=path),
                    )
                    self.assertEqual(result.status.value, "error")
                    self.assertTrue(result.message.startswith("output error:"))
                    self.assertEqual(result.preview, "")
                    self.assertIsNone(result.transcript_path)

            readable = root / "unreadable.md"
            readable.write_text("private", encoding="utf-8")
            with patch("pathlib.Path.read_text", side_effect=PermissionError("denied")):
                result = run_gui_request(
                    "https://youtu.be/gmj41fQTbfY",
                    output_dir=root,
                    pipeline=Mock(return_value=readable),
                )
            self.assertEqual(result.status.value, "error")
            self.assertTrue(result.message.startswith("output error:"))
            self.assertNotIn("denied", result.message)
            self.assertTrue(outside.exists())


if __name__ == "__main__":
    unittest.main()
