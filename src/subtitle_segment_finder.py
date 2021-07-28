import webvtt
from time_utils import convert_clock_time_to_timestamp_ms, convert_timestamp_ms_to_clock_time


class SubtitlePart:
    """A class that represents a part of the entire video's subtitle

    Attributes
    ----------
    start_time : int
        The starting time of this subtitle's part in milliseconds
    end_time : int
        The end time of this subtitle's part in milliseconds
    text : str
        The text corresponding to the subtitle's part
    """

    def __init__(self, start_time, end_time, text):
        self.start_time = start_time
        self.end_time = end_time
        self.text = text

    def __str__(self):
        return "{}-{}".format(self.start_time, self.end_time)

    def __repr__(self):
        return self.__str__()


class SubtitleWebVTTParser:
    """Parses the subtitles and its parts from a .vtt file

    Attributes
    ----------
    input_file : str
        The file path to the subtitles
    """

    def __init__(self, input_file):
        self.input_file = input_file

    def get_subtitle_parts(self):
        """Parses and gets the subtitle parts from the subtitle's file
           It also expands the subtitles in cases where there are gaps between subtitles

        Returns
        -------
        parts : SubtitlePart[]
            An ordered list of subtitle parts
        """
        parts = []
        for caption in webvtt.read(self.input_file):
            start_time = convert_clock_time_to_timestamp_ms(caption.start)
            end_time = convert_clock_time_to_timestamp_ms(caption.end)
            clean_text = self.__filter_text__(caption.text)

            parts.append(SubtitlePart(start_time, end_time, clean_text))

        # Extend certain subtitle times to fill in gaps
        for i in range(len(parts) - 1):
            cur = parts[i]
            next = parts[i + 1]

            if cur.end_time != next.start_time:
                cur.end_time = next.start_time

        return parts

    def __filter_text__(self, segment_text):
        """Takes in the text of a subtitle segment and cleans it"""
        return segment_text.replace("\n", " ").strip()


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

        for time_break in video_segment_end_times:
            pos = self.__get_part_position_of_time_break__(time_break)
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

    def __get_part_position_of_time_break__(self, time_break):
        part_index = self.__find_part__(time_break)

        # If the page_break_time > last fragment's time, then that page needs to capture the entire thing
        if time_break >= self.parts[-1].end_time:
            return len(self.parts) - 1, len(self.parts[-1].text) - 1            

        part = self.parts[part_index]

        # Get the char index in the fragment equal to the time_break
        ratio = (time_break - part.start_time) / (part.end_time - part.start_time)
        part_char_index = int(ratio * len(part.text))

        # Find the nearest position of a '.' left or right of our current position
        left_part_index = part_index
        left_part_char_index = part_char_index
        right_part_index = part_index
        right_part_char_index = part_char_index

        while (
            self.parts[left_part_index].text[left_part_char_index] != "."
            and self.parts[right_part_index].text[right_part_char_index] != "."
        ):
            left_part_char_index -= 1
            right_part_char_index += 1

            if left_part_char_index < 0:
                left_part_index = max(0, left_part_index - 1)
                left_part_char_index = len(self.parts[left_part_index].text) - 1

            if right_part_char_index >= len(self.parts[right_part_index].text):
                right_part_index = min(len(self.parts) - 1, right_part_index + 1)
                right_part_char_index = 0

        if self.parts[left_part_index].text[left_part_char_index] == ".":
            return left_part_index, left_part_char_index

        elif self.parts[right_part_index].text[right_part_char_index] == ".":
            return right_part_index, right_part_char_index

        else:
            raise Exception("Cannot find '.' in fragment index {}".format(part_index))

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
    parser = SubtitleWebVTTParser("../tests/subtitles/subtitles_1.vtt")
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
