import unittest
import snapshottest
from src.time_utils import convert_clock_time_to_timestamp_ms as get_timestamp
from src.subtitle_segment_finder import SubtitleSegmentFinder
from src.subtitle_part import SubtitlePart
from src.subtitle_webvtt_parser import SubtitleWebVTTParser
from src.subtitle_srt_parser import SubtitleSRTParser


class SubtitleSplitterTests(snapshottest.TestCase):
    def test_get_pages_given_subtitle_without_periods_and_future_timestamp_should_return_correct_pages(
        self,
    ):
        segments = [
            SubtitlePart(
                get_timestamp("00:00:00"),
                get_timestamp("00:00:10"),
                "hi there my name is Bob",
            )
        ]
        pager = SubtitleSegmentFinder(segments)
        time_breaks = [get_timestamp("00:00:14")]
        transcript_pages = pager.get_subtitle_segments(time_breaks)

        self.assertEqual(transcript_pages[0], "hi there my name is Bob")

    def test_get_pages_given_subtitle_without_periods_and_middle_timestamp_should_return_correct_pages(
        self,
    ):
        segments = [
            SubtitlePart(
                get_timestamp("00:00:00"),
                get_timestamp("00:00:10"),
                "hi there my name is Bob",
            )
        ]
        pager = SubtitleSegmentFinder(segments)
        time_breaks = [get_timestamp("00:00:05")]
        transcript_pages = pager.get_subtitle_segments(time_breaks)

        self.assertEqual(transcript_pages[0], "hi there my")

    def test_get_pages_given_subtitle_without_periods_and_past_timestamp_should_return_correct_pages(
        self,
    ):
        segments = [
            SubtitlePart(
                get_timestamp("00:00:10"),
                get_timestamp("00:00:20"),
                "hi there my name is Bob",
            )
        ]
        pager = SubtitleSegmentFinder(segments)
        time_breaks = [get_timestamp("00:00:05")]
        transcript_pages = pager.get_subtitle_segments(time_breaks)

        self.assertEqual(transcript_pages[0], "")

    def test_get_pages_given_subtitle_with_period_should_return_correct_pages(self):
        segments = [
            SubtitlePart(
                get_timestamp("00:00:00"),
                get_timestamp("00:00:10"),
                "Hi. My name is Bob",
            )
        ]
        pager = SubtitleSegmentFinder(segments)
        time_breaks = [get_timestamp("00:00:05")]
        transcript_pages = pager.get_subtitle_segments(time_breaks)
        self.assertEqual(transcript_pages[0], "Hi.")

    def test_get_pages_given_multiple_subtitle_segments_should_return_correct_pages(
        self,
    ):
        segments = [
            SubtitlePart(
                get_timestamp("00:00:00"),
                get_timestamp("00:00:10"),
                "Hi. My name is Bob",
            ),
            SubtitlePart(
                get_timestamp("00:00:10"),
                get_timestamp("00:00:20"),
                "and his name is Alice. Today, we are",
            ),
        ]
        pager = SubtitleSegmentFinder(segments)
        time_breaks = [get_timestamp("00:00:02"), get_timestamp("00:00:15")]
        transcript_pages = pager.get_subtitle_segments(time_breaks)

        self.assertEqual(transcript_pages[0], "Hi.")
        self.assertEqual(transcript_pages[1], "My name is Bob and his name is Alice.")

    def test_get_pages_given_multiple_subtitle_segments_when_selecting_subtitle_at_break_should_return_correct_pages(
        self,
    ):
        segments = [
            SubtitlePart(
                get_timestamp("00:00:00"),
                get_timestamp("00:00:10"),
                "Hi. My name is Bob",
            ),
            SubtitlePart(
                get_timestamp("00:00:10"),
                get_timestamp("00:00:20"),
                "and his name is Alice. Today, we are",
            ),
        ]
        pager = SubtitleSegmentFinder(segments)
        time_breaks = [get_timestamp("00:00:10"), get_timestamp("00:00:20")]
        transcript_pages = pager.get_subtitle_segments(time_breaks)

        self.assertEqual(len(transcript_pages), 2)
        self.assertEqual(transcript_pages[0], "Hi.")
        self.assertEqual(
            transcript_pages[1], "My name is Bob and his name is Alice. Today, we are"
        )

    def test_get_pages_given_subtitle_1_should_return_correct_pages(self):
        segments = SubtitleWebVTTParser(
            "tests/subtitles/subtitles_1.vtt"
        ).get_subtitle_parts()
        pager = SubtitleSegmentFinder(segments)

        breaks = [
            get_timestamp("00:00:14"),
            get_timestamp("00:02:10"),
            get_timestamp("00:05:38"),
            get_timestamp("00:07:58"),
            get_timestamp("00:10:37"),
            get_timestamp("00:10:52"),
            get_timestamp("00:10:54"),
        ]
        transcript_pages = pager.get_subtitle_segments(breaks)

        self.assertEqual(len(transcript_pages), 7)
        self.assertMatchSnapshot(transcript_pages)

    def test_get_pages_given_subtitle_8_should_return_correct_pages(self):
        segments = SubtitleSRTParser(
            "tests/subtitles/subtitles_8.srt"
        ).get_subtitle_parts()
        pager = SubtitleSegmentFinder(segments)

        breaks = [
            get_timestamp("00:00:04"),
            get_timestamp("00:00:05"),
            get_timestamp("00:00:06"),
            get_timestamp("00:00:07"),
            get_timestamp("00:00:08"),
            get_timestamp("00:00:09"),
            get_timestamp("00:00:15"),
            get_timestamp("00:00:23"),
            get_timestamp("00:00:26"),
            get_timestamp("00:00:27"),
            get_timestamp("00:00:31"),
            get_timestamp("00:00:41"),
            get_timestamp("00:00:45"),
            get_timestamp("00:00:53"),
            get_timestamp("00:01:03"),
            get_timestamp("00:01:25"),
            get_timestamp("00:01:47"),
            get_timestamp("00:04:00"),
            get_timestamp("00:04:30"),
            get_timestamp("00:05:15"),
            get_timestamp("00:05:58"),
            get_timestamp("00:07:33"),
            get_timestamp("00:08:04"),
            get_timestamp("00:08:24"),
            get_timestamp("00:09:02"),
            get_timestamp("00:09:42"),
            get_timestamp("00:10:00"),
        ]
        transcript_pages = pager.get_subtitle_segments(breaks)

        self.assertEqual(len(transcript_pages), 27)
        self.assertMatchSnapshot(transcript_pages)

    def test_get_pages_given_subtitles_with_no_dots_should_return_correct_pages(self):
        segments = [
            SubtitlePart(
                get_timestamp("00:00:00"),
                get_timestamp("00:00:10"),
                "Hi my name is Bob",
            ),
            SubtitlePart(
                get_timestamp("00:00:10"),
                get_timestamp("00:00:20"),
                "and his name is Alice Today, we are",
            ),
        ]
        pager = SubtitleSegmentFinder(segments)
        time_breaks = [get_timestamp("00:00:08"), get_timestamp("00:00:20")]
        transcript_pages = pager.get_subtitle_segments(time_breaks)

        self.assertEqual(len(transcript_pages), 2)
        self.assertEqual(transcript_pages[0], "Hi my name is")
        self.assertEqual(transcript_pages[1], "Bob and his name is Alice Today, we are")
