import os
import cv2
from fpdf import FPDF
import tempfile

from .subtitle_webvtt_parser import SubtitleWebVTTParser
from .subtitle_segment_finder import SubtitleSegmentFinder
from .video_segment_finder import VideoSegmentFinder


class ContentSegment:
    """This class represents the image and the text that represents one segment of the video
    For instance, an image could be a powerpoint slide and the text could be the explaination of that slide

    Attributes
    ----------
    image : np.array(x, y, 3)
        The image
    text : str
        The text
    """

    def __init__(self, image, text):
        self.image = image
        self.text = text


class ContentSegmentPdfBuilder:
    """This class creates a PDF from a lecture segment"""

    def generate_pdf(self, pages, output_filepath):
        """Generates and saves a PDF from an ordered list of lecture segments

        Parameters
        ----------
        pages : ContentSegment[]
            An ordered list of lecture segments
        output_filepath: str
            The filepath for the output pdf
        """
        with tempfile.TemporaryDirectory() as temp_dir_path:
            pdf = FPDF()
            pdf.add_font("DejaVu", "", "fonts/DejaVuSansCondensed.ttf", uni=True)

            for i in range(0, len(pages)):
                # Temporarily save the frames
                temp_filepath = os.path.join(temp_dir_path, f"{i}_frame.jpeg")
                cv2.imwrite(temp_filepath, pages[i].image)

                pdf.add_page()

                # Add the image
                pdf.image(temp_filepath, w=195)

                # Add the captions if exist
                if pages[i].text is not None:
                    pdf.set_font("DejaVu", "", 12)
                    pdf.multi_cell(0, 10, pages[i].text)

            pdf.output(output_filepath, "F")


if __name__ == "__main__":
    # Get the selected frames
    selected_frames_data = VideoSegmentFinder().get_best_segment_frames(
        "../tests/videos/input_1.mp4"
    )
    frame_nums = sorted(selected_frames_data.keys())
    selected_frames = [selected_frames_data[i]["frame"] for i in frame_nums]

    # Get the subtitles for each frame
    pager = SubtitleSegmentFinder(
        SubtitleWebVTTParser("../tests/subtitles/subtitles_1.vtt").get_subtitle_parts()
    )
    subtitle_breaks = [selected_frames_data[i]["timestamp"] for i in frame_nums]
    pages = pager.get_subtitle_segments(subtitle_breaks)

    # Merge the frame and subtitles for each frame to create a pdf
    video_subtitle_pages = []

    for i in range(0, len(selected_frames)):
        frame = selected_frames[i]
        subtitle_page = pages[i]
        video_subtitle_pages.append(ContentSegment(frame, subtitle_page))

    printer = ContentSegmentPdfBuilder()
    pdf = printer.generate_pdf(video_subtitle_pages, "myfile.pdf")
