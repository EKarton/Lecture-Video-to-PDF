from subtitle_webvtt_parser import SubtitleWebVTTParser


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
