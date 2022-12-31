import webvtt
from .subtitle_part import SubtitlePart
from .time_utils import convert_clock_time_to_timestamp_ms

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

            if len(clean_text) == 0:
                continue

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
