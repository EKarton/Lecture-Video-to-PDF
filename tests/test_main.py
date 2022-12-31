import tempfile
from src.main import CommandLineArgRunner
from unittest import mock, TestCase
from parameterized import parameterized
from tests.utils.pdf_snapshot import assert_match_pdf_snapshot


@mock.patch("time.time", mock.MagicMock(return_value=12345))
class MainTests(TestCase):
    @parameterized.expand(
        [
            ("input_1.mp4", "subtitles_1.srt", "video_1_with_srt_file.pdf"),
            ("input_1.mp4", "subtitles_1.vtt", "video_1_with_webvtt_file.pdf"),
            ("input_2.mp4", "subtitles_2.srt", "video_2_with_srt_file.pdf"),
            ("input_2.mp4", "subtitles_2.vtt", "video_2_with_webvtt_file.pdf"),
            ("input_7.mp4", "subtitles_7.srt", "video_7_with_srt_file.pdf"),
            ("input_8.mp4", "subtitles_8.srt", "video_8_with_srt_file.pdf"),
            ("input_8.mp4", "subtitles_8.vtt", "video_8_with_webvtt_file.pdf"),
        ]
    )
    def test_run_given_video_and_subtitles_should_generate_pdf_correctly(
        self, video_filename, subtitle_filename, output_filename
    ):
        test_output_file = tempfile.NamedTemporaryFile(suffix=".pdf")

        cli = CommandLineArgRunner()
        cli.run(
            [
                f"tests/videos/{video_filename}",
                "-s",
                f"tests/subtitles/{subtitle_filename}",
                "-o",
                test_output_file.name,
            ]
        )

        assert_match_pdf_snapshot(
            f"tests/snapshots/snap_test_main/{output_filename}",
            test_output_file.name,
        )

    @parameterized.expand(
        [
            ("input_1.mp4", "video_1_without_subtitles.pdf"),
            ("input_2.mp4", "video_2_without_subtitles.pdf"),
            ("input_7.mp4", "video_7_without_subtitles.pdf"),
            ("input_8.mp4", "video_8_without_subtitles.pdf"),
        ]
    )
    def test_run_given_video_and_skip_subtitles_flag_should_generate_pdf_correctly(
        self, video_filename, output_filename
    ):
        test_output_file = tempfile.NamedTemporaryFile(suffix=".pdf")

        cli = CommandLineArgRunner()
        cli.run(
            [
                f"tests/videos/{video_filename}",
                "-S",
                "-o",
                test_output_file.name,
            ]
        )

        assert_match_pdf_snapshot(
            f"tests/snapshots/snap_test_main/{output_filename}",
            test_output_file.name,
        )

    def test_run_given_video_and_subtitles_and_skip_subtitles_flag_should_throw_error(
        self,
    ):
        test_output_file = tempfile.NamedTemporaryFile(suffix=".pdf")

        cli = CommandLineArgRunner()
        func_to_test = lambda: cli.run(
            [
                "tests/videos/input_1.mp4",
                "-S",
                "-s",
                "tests/subtitles/subtitles_1.srt",
                "-o",
                test_output_file.name,
            ]
        )

        self.assertRaises(AssertionError, func_to_test)
