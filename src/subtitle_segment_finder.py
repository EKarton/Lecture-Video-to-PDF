from .subtitle_webvtt_parser import SubtitleWebVTTParser
from .subtitle_srt_parser import SubtitleSRTParser


class SubtitleGenerator:
    def __init__(self, video_file):
        self.video_file = video_file

    def get_segments(self):
        pass


class SubtitleSegmentFinder:
    """This class finds the best subtitle segments from the end times of video segments"""

    def __init__(self, parts):
        self.parts = parts

    def get_subtitle_segments(self, video_segment_end_times):
        """Returns the subtitles of video segments given the end times of each video segment

        For instance, given times:
            [ "00:00:10", "00:00:20", "00:00:30" ]
        it will return the subtitles for times:
            00:00:00 - 00:00:10
            00:00:10 - 00:00:20
            00:00:20 - 00:00:30

        Parameters
        ----------
        video_segment_end_times : int[]
            A list of timestamps representing the end times of each video segment

        Returns
        -------
        segments : str[]
            A list of subtitle segments
        """
        part_positions = []

        for i in range(len(video_segment_end_times)):
            time_break = video_segment_end_times[i]

            prev_time_break = 0
            if i > 0:
                prev_time_break = video_segment_end_times[i - 1]

            next_time_break = float('inf')
            if i < len(video_segment_end_times) - 1:
                next_time_break =  video_segment_end_times[i + 1]

            pos = self.__get_part_position_of_time_break__(time_break, prev_time_break, next_time_break)
            part_positions.append(pos)

        start_pos = (0, 0)
        segments = []
        for end_pos in part_positions:
            segment = None

            if start_pos[0] > end_pos[0]:
                segment = ""

            elif start_pos[0] == end_pos[0] and start_pos[1] > end_pos[1]:
                segment = ""

            elif start_pos[0] == end_pos[0] and start_pos[1] <= end_pos[1]:
                segment = self.parts[start_pos[0]].text[start_pos[1] : end_pos[1] + 1]

            elif start_pos[0] < end_pos[0]:
                segment = " ".join(
                    [self.parts[start_pos[0]].text[start_pos[1] :].strip()]
                    + [self.parts[i].text for i in range(start_pos[0] + 1, end_pos[0])]
                    + [self.parts[end_pos[0]].text[0 : end_pos[1] + 1].strip()]
                )

            segment = segment.strip()

            start_pos = (end_pos[0], end_pos[1] + 1)

            segments.append(segment)

        return segments

    def __get_part_position_of_time_break__(self, time_break, min_time_break, max_time_break):
        min_part_idx = self.__find_part__(min_time_break)
        max_part_idx = self.__find_part__(max_time_break)
        part_index = self.__find_part__(time_break)

        if min_part_idx is None:
            min_part_idx = 0

        if max_part_idx is None:
            max_part_idx = len(self.parts)

        # If the page_break_time > last fragment's time, then that page needs to capture the entire thing
        if time_break >= self.parts[-1].end_time:
            return len(self.parts) - 1, len(self.parts[-1].text) - 1

        if part_index is None:
            return 0, -1

        part = self.parts[part_index]

        # Get the char index in the fragment equal to the time_break
        ratio = (time_break - part.start_time) / (part.end_time - part.start_time)
        part_char_index = int(ratio * len(part.text))

        # Find the nearest position of a '.' left or right of 'part_index' and 'part_char_index'
        left_part_index = part_index
        left_part_char_index = part_char_index
        right_part_index = part_index
        right_part_char_index = part_char_index

        while left_part_index >= min_part_idx and right_part_index < max_part_idx:
            if self.parts[left_part_index].text[left_part_char_index] == ".":
                return left_part_index, left_part_char_index

            if self.parts[right_part_index].text[right_part_char_index] == ".":
                return right_part_index, right_part_char_index

            left_part_char_index -= 1
            right_part_char_index += 1

            if left_part_char_index < 0:
                left_part_index -= 1
                left_part_char_index = len(self.parts[left_part_index].text) - 1

            if right_part_char_index >= len(self.parts[right_part_index].text):
                right_part_index += 1
                right_part_char_index = 0

        while left_part_index >= min_part_idx:
            if self.parts[left_part_index].text[left_part_char_index] == ".":
                return left_part_index, left_part_char_index

            left_part_char_index -= 1

            if left_part_char_index < 0:
                left_part_index -= 1
                left_part_char_index = len(self.parts[left_part_index].text) - 1

        while right_part_index < max_part_idx:
            if self.parts[right_part_index].text[right_part_char_index] == ".":
                return right_part_index, right_part_char_index

            right_part_char_index += 1

            if right_part_char_index >= len(self.parts[right_part_index].text):
                right_part_index += 1
                right_part_char_index = 0

        # Fallback: return the found part index and part char
        return part_index, part_char_index

    def __find_part__(self, timestamp_ms):
        left = 0
        right = len(self.parts) - 1

        while left <= right:
            mid = (left + right) // 2
            cur_part = self.parts[mid]

            if cur_part.start_time <= timestamp_ms < cur_part.end_time:
                return mid
            elif timestamp_ms < cur_part.start_time:
                right = mid - 1
            else:
                left = mid + 1

        return None


if __name__ == "__main__":

    def test1():
        parser = SubtitleWebVTTParser("../tests/subtitles/subtitles_2.vtt")
        parts = parser.get_subtitle_parts()
        segment_finder = SubtitleSegmentFinder(parts)

        breaks = [14000, 130000, 338000, 478000, 637000, 652000, 654000]

        """ We will have transcriptions at these times:
            > 0 - 14000
            > 14000 - 130000
            > 130000 - 338000
            > 338000 - 478000
            > 478000 - 637000
            > 637000 - 652000
            > 652000 - 654000
        """
        transcript_pages = segment_finder.get_subtitle_segments(breaks)

        print(len(transcript_pages))
        for transcript_page in transcript_pages:
            print("-----------------------")
            print(transcript_page)
            print("-----------------------")

    def test2():
        parser = SubtitleSRTParser("../tests/subtitles/subtitles_7.srt")
        parts = parser.get_subtitle_parts()
        print(len(parts))
        segment_finder = SubtitleSegmentFinder(parts)

        breaks = [
            10520.0,
            103680.0,
            143360.0,
            773040.0,
            1118240.0,
            1693000.0,
            1704760.0,
        ]

        """ We will have transcriptions at these times:
            > 0 - 14000
            > 14000 - 130000
            > 130000 - 338000
            > 338000 - 478000
            > 478000 - 637000
            > 637000 - 652000
            > 652000 - 654000
        """
        transcript_pages = segment_finder.get_subtitle_segments(breaks)

        print(len(transcript_pages))
        for transcript_page in transcript_pages:
            print("-----------------------")
            print(transcript_page)
            print("-----------------------")

    test2()
