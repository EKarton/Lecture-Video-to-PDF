import tempfile
import unittest
from src.time_utils import convert_clock_time_to_timestamp_ms as get_timestamp
from src.subtitle_srt_parser import SubtitleSRTParser


class SubtitleSRTParserTests(unittest.TestCase):
    def test_get_subtitle_parts_given_subtitles_should_return_correct_subtitles(self):
        with tempfile.NamedTemporaryFile(mode="w+", encoding="utf-8") as tmpFile:
            tmpFile.writelines(
                [
                    "1\n",
                    "00:00:00,000 --> 00:00:04,134\n",
                    "So now that we understand what a secure\n",
                    "PRG is, and we understand what semantic\n",
                    "\n",
                    "2\n",
                    "00:00:04,134 --> 00:00:08,425\n",
                    "security means, we can actually argue that\n",
                    "a stream cipher with a secure PRG is, in\n",
                ]
            )
            tmpFile.flush()

            segments = SubtitleSRTParser(tmpFile.name).get_subtitle_parts()

            self.assertEqual(len(segments), 2)
            self.assertEqual(segments[0].start_time, get_timestamp("00:00:00"))
            self.assertEqual(segments[0].end_time, get_timestamp("00:00:04.134"))
            self.assertEqual(
                segments[0].text,
                "So now that we understand what a secure PRG is, and we understand what semantic",
            )

            self.assertEqual(segments[1].start_time, get_timestamp("00:00:04.134"))
            self.assertEqual(segments[1].end_time, get_timestamp("00:00:08.425"))
            self.assertEqual(
                segments[1].text,
                "security means, we can actually argue that a stream cipher with a secure PRG is, in",
            )

    def test_get_subtitle_parts_given_subtitles_with_no_text_should_not_include_empty_subtitles(
        self,
    ):
        with tempfile.NamedTemporaryFile(mode="w+", encoding="utf-8") as tmpFile:
            tmpFile.writelines(
                [
                    "1\n",
                    "00:00:00,000 --> 00:00:04,134\n",
                    "So now that we understand what a secure\n",
                    "PRG is, and we understand what semantic\n",
                    "\n",
                    "2\n",
                    "00:00:04,134 --> 00:00:10,134\n",
                    "\n",
                    "\n",
                    "\n",
                    "3\n",
                    "00:00:10,134 --> 00:00:18,425\n",
                    "security means, we can actually argue that\n",
                    "a stream cipher with a secure PRG is, in\n",
                ]
            )
            tmpFile.flush()

            segments = SubtitleSRTParser(tmpFile.name).get_subtitle_parts()

            self.assertEqual(len(segments), 2)
            self.assertEqual(segments[0].start_time, get_timestamp("00:00:00"))
            self.assertEqual(segments[0].end_time, get_timestamp("00:00:10.134"))
            self.assertEqual(
                segments[0].text,
                "So now that we understand what a secure PRG is, and we understand what semantic",
            )

            self.assertEqual(segments[1].start_time, get_timestamp("00:00:10.134"))
            self.assertEqual(segments[1].end_time, get_timestamp("00:00:18.425"))
            self.assertEqual(
                segments[1].text,
                "security means, we can actually argue that a stream cipher with a secure PRG is, in",
            )

    def test_get_subtitle_parts_given_subtitles_that_are_not_continuous_should_return_correct_subtitles(
        self,
    ):
        with tempfile.NamedTemporaryFile(mode="w+", encoding="utf-8") as tmpFile:
            tmpFile.writelines(
                [
                    "1\n",
                    "00:00:00,000 --> 00:00:04,134\n",
                    "So now that we understand what a secure\n",
                    "PRG is, and we understand what semantic\n",
                    "\n",
                    "2\n",
                    "00:00:04,134 --> 00:00:08,425\n",
                    "security means, we can actually argue that\n",
                    "a stream cipher with a secure PRG is, in\n",
                ]
            )
            tmpFile.flush()

            segments = SubtitleSRTParser(tmpFile.name).get_subtitle_parts()

            self.assertEqual(len(segments), 2)
            self.assertEqual(segments[0].start_time, get_timestamp("00:00:00"))
            self.assertEqual(segments[0].end_time, get_timestamp("00:00:04.134"))
            self.assertEqual(
                segments[0].text,
                "So now that we understand what a secure PRG is, and we understand what semantic",
            )

            self.assertEqual(segments[1].start_time, get_timestamp("00:00:04.134"))
            self.assertEqual(segments[1].end_time, get_timestamp("00:00:08.425"))
            self.assertEqual(
                segments[1].text,
                "security means, we can actually argue that a stream cipher with a secure PRG is, in",
            )
