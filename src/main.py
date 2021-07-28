import sys
import argparse
from subtitle_segment_finder import (
    SubtitleWebVTTParser,
    SubtitleGenerator,
    SubtitleSegmentFinder,
)
from video_segment_finder import VideoSegmentFinder
from content_segment_exporter import ContentSegment, ContentSegmentPdfBuilder


class CommandLineArgRunner:
    def __init__(self):
        self.parser = argparse.ArgumentParser(
            description="Generate a readable pdf from lecture videos"
        )
        self.parser.add_argument("video", type=str, help="File path to lecture video")
        self.parser.add_argument(
            "-s",
            "--subtitle",
            type=str,
            default=None,
            help="File path to video subtitle. If omitted, it will generate subtitles",
        )
        self.parser.add_argument(
            "-o",
            "--output",
            type=str,
            default="output.pdf",
            help="Output file to generated pdf",
        )

    def run(self, args):
        opts = self.parser.parse_args(args)

        video_filepath = opts.video
        subtitle_filepath = opts.subtitle
        output_filepath = opts.output

        subtitle_parser = SubtitleWebVTTParser(subtitle_filepath)
        if subtitle_filepath == None:
            subtitle_parser = SubtitleGenerator(video_filepath)

        video_segment_finder = VideoSegmentFinder()

        self.__run__(
            video_segment_finder, video_filepath, subtitle_parser, output_filepath
        )

    def __run__(
        self, video_segment_finder, video_filepath, subtitle_parser, output_filepath
    ):
        # Get the selected frames
        print('Getting selected frames')
        selected_frames_data = video_segment_finder.get_best_segment_frames(video_filepath)
        frame_nums = sorted(selected_frames_data.keys())
        selected_frames = [selected_frames_data[i]["frame"] for i in frame_nums]

        # Get the subtitles for each frame
        print('Getting subtitles for each frame')
        segment_finder = SubtitleSegmentFinder(subtitle_parser.get_subtitle_parts())
        subtitle_breaks = [selected_frames_data[i]["timestamp"] for i in frame_nums]
        segments = segment_finder.get_subtitle_segments(subtitle_breaks)

        # Merge the frame and subtitles for each frame to create a pdf
        print('Merging frames and subtitles')
        video_subtitle_pages = []

        for i in range(0, len(selected_frames)):
            frame = selected_frames[i]
            subtitle_page = segments[i]
            video_subtitle_pages.append(ContentSegment(frame, subtitle_page))

        printer = ContentSegmentPdfBuilder()
        pdf = printer.generate_pdf(video_subtitle_pages, output_filepath)


if __name__ == "__main__":
    runner = CommandLineArgRunner()
    runner.run(sys.argv[1:])
