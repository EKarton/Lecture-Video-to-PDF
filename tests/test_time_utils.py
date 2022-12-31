import unittest
from src.time_utils import convert_timestamp_ms_to_clock_time as get_clock_time
from src.time_utils import convert_clock_time_to_timestamp_ms as get_timestamp


class TimeUtilsTests(unittest.TestCase):
    def test_given_hh_mm_ss_it_should_convert_to_clock_time_correctly(self):
        self.assertEqual(get_clock_time(7538000), "02:05:38")

    def test_given_mm_ss_it_should_convert_to_clock_time_correctly(self):
        self.assertEqual(get_clock_time(338000), "00:05:38")

    def test_given_seconds_it_should_convert_to_clock_time_correctly(self):
        self.assertEqual(get_clock_time(38456), "00:00:38.456")

    def test_given_zero_seconds_it_should_convert_to_clock_time_correctly(self):
        self.assertEqual(get_clock_time(456), "00:00:00.456")

    def test_given_timestamp_ms_with_hours_it_should_convert_to_timestamp_ms_correctly(
        self,
    ):
        self.assertEqual(get_timestamp("02:05:38"), 7538000)

    def test_given_time_without_hours_it_should_convert_to_timestamp_ms_correctly(self):
        self.assertEqual(get_timestamp("00:05:38"), 338000)

    def test_given_time_minutes_or_hours_it_should_convert_to_timestamp_ms_correctly(
        self,
    ):
        self.assertEqual(get_timestamp("00:00:38.456"), 38456)

    def test_given_zero_seconds_it_should_convert_to_timestamp_ms_correctly(self):
        self.assertEqual(get_timestamp("00:00:00.456"), 456)
