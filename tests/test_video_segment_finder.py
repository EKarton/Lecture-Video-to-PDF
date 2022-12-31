import unittest
from src.video_segment_finder import VideoSegmentFinder  # get_frames
from src.time_utils import convert_timestamp_ms_to_clock_time as get_clock


class VideoBreaksTest(unittest.TestCase):
    def test_get_frames_of_video_with_human_should_return_correct_breaks(self):
        data = VideoSegmentFinder().get_best_segment_frames("tests/videos/input_1.mp4")
        # data = get_frames('videos/input_1.mp4')
        frame_nums = sorted(data.keys())

        self.assertEqual(len(frame_nums), 7)

        # Check if the timestamps (in ms) matches the ones that we picked out manually
        self.assertEqual(
            get_clock(data[frame_nums[0]]["timestamp"]), "00:00:14.147480814147482"
        )
        self.assertEqual(
            get_clock(data[frame_nums[1]]["timestamp"]), "00:02:10.330330330330325"
        )
        self.assertEqual(
            get_clock(data[frame_nums[2]]["timestamp"]), "00:05:38.071404738071436"
        )
        self.assertEqual(
            get_clock(data[frame_nums[3]]["timestamp"]), "00:07:58.41174507841177"
        )
        self.assertEqual(
            get_clock(data[frame_nums[4]]["timestamp"]), "00:10:37.53753753753752"
        )
        self.assertEqual(
            get_clock(data[frame_nums[5]]["timestamp"]), "00:10:52.05205205205211"
        )
        self.assertEqual(
            get_clock(data[frame_nums[6]]["timestamp"]), "00:10:54.38772105438775"
        )

    def test_get_frames_of_video_without_human_should_return_correct_breaks(self):
        data = VideoSegmentFinder().get_best_segment_frames("tests/videos/input_2.mp4")
        frame_nums = sorted(data.keys())

        self.assertEqual(len(frame_nums), 7)

        # Check if the timestamps (in ms) matches the ones that we picked out manually
        self.assertEqual(
            get_clock(data[frame_nums[0]]["timestamp"]), "00:00:04.337671004337671"
        )
        self.assertEqual(
            get_clock(data[frame_nums[1]]["timestamp"]), "00:00:49.215882549215884"
        )
        self.assertEqual(
            get_clock(data[frame_nums[2]]["timestamp"]), "00:04:10.784117450784136"
        )
        self.assertEqual(
            get_clock(data[frame_nums[3]]["timestamp"]), "00:07:59.01234567901236"
        )
        self.assertEqual(
            get_clock(data[frame_nums[4]]["timestamp"]), "00:11:09.669669669669704"
        )
        self.assertEqual(
            get_clock(data[frame_nums[5]]["timestamp"]), "00:12:24.878211544878198"
        )
        self.assertEqual(
            get_clock(data[frame_nums[6]]["timestamp"]), "00:12:34.788121454788254"
        )

    def test_get_frames_of_video_with_lots_of_animations_should_return_correct_breaks(
        self,
    ):
        data = VideoSegmentFinder().get_best_segment_frames("tests/videos/input_3.mp4")
        frame_nums = sorted(data.keys())

        self.assertEqual(len(frame_nums), 12)

        # Check if the timestamps (in ms) matches the ones that we picked out manually
        self.assertEqual(
            get_clock(data[frame_nums[0]]["timestamp"]), "00:00:37.69527777777778"
        )
        self.assertEqual(
            get_clock(data[frame_nums[1]]["timestamp"]), "00:00:56.49292222222223"
        )
        self.assertEqual(
            get_clock(data[frame_nums[2]]["timestamp"]), "00:01:13.5407888888889"
        )
        self.assertEqual(
            get_clock(data[frame_nums[3]]["timestamp"]), "00:01:43.53703333333334"
        )
        self.assertEqual(
            get_clock(data[frame_nums[4]]["timestamp"]), "00:02:57.783333333333346"
        )
        self.assertEqual(
            get_clock(data[frame_nums[5]]["timestamp"]), "00:03:33.183333333333344"
        )
        self.assertEqual(
            get_clock(data[frame_nums[6]]["timestamp"]), "00:03:45.98333333333334"
        )
        self.assertEqual(
            get_clock(data[frame_nums[7]]["timestamp"]), "00:03:59.183333333333344"
        )
        self.assertEqual(
            get_clock(data[frame_nums[8]]["timestamp"]), "00:04:09.833333333333343"
        )
        self.assertEqual(
            get_clock(data[frame_nums[9]]["timestamp"]), "00:04:42.48333333333337"
        )
        self.assertEqual(
            get_clock(data[frame_nums[10]]["timestamp"]), "00:05:52.933333333333316"
        )
        self.assertEqual(
            get_clock(data[frame_nums[11]]["timestamp"]), "00:06:40.98333333333337"
        )

    def test_get_frames_of_video_with_blur_animations_should_return_correct_breaks(
        self,
    ):
        data = VideoSegmentFinder().get_best_segment_frames("tests/videos/input_4.mp4")
        frame_nums = sorted(data.keys())

        self.assertEqual(len(frame_nums), 2)

        # Check if the timestamps (in ms) matches the ones that we picked out manually
        self.assertEqual(
            get_clock(data[frame_nums[0]]["timestamp"]), "00:00:03.7495333333333334"
        )
        self.assertEqual(
            get_clock(data[frame_nums[1]]["timestamp"]), "00:00:07.649044444444445"
        )

    def test_get_frames_of_video_with_blur_annotations_should_return_correct_breaks(
        self,
    ):
        data = VideoSegmentFinder().get_best_segment_frames("tests/videos/input_5.mp4")
        frame_nums = sorted(data.keys())

        self.assertEqual(len(frame_nums), 2)

        # Check if the timestamps (in ms) matches the ones that we picked out manually
        self.assertEqual(
            get_clock(data[frame_nums[0]]["timestamp"]), "00:01:54.34768101434769"
        )
        self.assertEqual(
            get_clock(data[frame_nums[1]]["timestamp"]), "00:02:25.47881214547882"
        )

    def test_get_frames_of_video_with_add_animations_should_return_correct_breaks(self):
        data = VideoSegmentFinder().get_best_segment_frames("tests/videos/input_6.mp4")
        frame_nums = sorted(data.keys())

        self.assertEqual(len(frame_nums), 3)

        # Check if the timestamps (in ms) matches the ones that we picked out manually
        self.assertEqual(get_clock(data[frame_nums[0]]["timestamp"]), "00:01:31.15")
        self.assertEqual(
            get_clock(data[frame_nums[1]]["timestamp"]), "00:01:34.850000000000016"
        )
        self.assertEqual(get_clock(data[frame_nums[2]]["timestamp"]), "00:01:41.5")
