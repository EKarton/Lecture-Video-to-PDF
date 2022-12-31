# Convert Lecture Videos to PDF

### Description

Want to go through lecture videos faster without missing any information? Wish you can **read** the lecture video instead of watching it? Now you can! With this python app, you can convert lecture videos to PDF files! The PDF file will contain a screenshot of lecture slides presented in the video, along with a transcription of your instructor explaining those lecture slide. It can also handle instructors making annotations on their lecture slides and mild amounts of PowerPoint animations.

### Table of Contents

- Walkthrough
- Getting Started
- Tweeking the Application
- Next steps
- Usage
- Credits
- License

### Walkthrough of this project

Users will need to download a video file of their lecture. For instance, the video file might look like this:

<div width="100%">
    <p align="center">
<img src="docs/video-screenshot.png" width="600px"/>
    </p>
</div>

Users will also need a copy of the video's subtitles.

After running the command line tool, they will get a PDF that looks like this:

<div width="100%">
    <p align="center">
<img src="docs/pdf-screenshot.png" width="600px"/>
    </p>
</div>

where each page contains an image of the lecture video, and a transcription of the instructor explaining about that slide.

### Getting Started

1. Ensure Python3 and Pip is installed on your machine
2. Next, install package dependencies by running:

   `pip3 install -r requirements.txt`

3. Now, run:

   `python3 -m src.main tests/videos/input_1.mp4 -s tests/subtitles/subtitles_1.vtt -o output.pdf`

   to generate a PDF of [this lecture video](tests/videos/input_1.mp4) with [these subtitles](```tests/subtitles/subtitles_1.vtt```)

   Note: If you don't want subtitles in the pdf, you can use the `-S` flag, like:

      `python3 -m src.main tests/videos/input_1.mp4 -S -o output.pdf`

4. The generated PDF will be saved as _output.pdf_

### Running Tests

1. Install graphicsmagick, imagemagick, and pdftk on your machine
2. To run all unit tests, run `python3 -m unittest discover`
3. To run a specific unit tests (ex: tests/test_main.py), run `python3 -m unittest tests/test_main.py`

Note: Running the `tests/test_main.py` takes a while

### Tweeking the Application

This application uses computer vision with OpenCV to detect when the instructor has moved on to the next PowerPoint slide, detect animations, etc.

You can adjust the sensitivity to video frame changes in the `src/video_segment_finder.py` file. You can also visualize how well the application detect transitions and animations via the `src/plot.py` tool.

### Next Steps

- [ ] Automatically generate subtitles
- [ ] Wrap project into a web app?

### Usage

Please note that this project is used for educational purposes and is not intended to be used commercially. We are not liable for any damages/changes done by this project.

### Credits

Emilio Kartono, who made the entire project.

The fonts for generating the PDF is from [DejaVu fonts](https://dejavu-fonts.github.io/)

### License

This project is protected under the GNU licence. Please refer to the LICENSE.txt for more information.
