import tempfile
import os
from os import path
import shutil
import pypdftk
from wand.image import Image


def assert_match_pdf_snapshot(expected_filepath, actual_filepath, max_diff_val=0.0):
    """Verifies if the pdf matches the expected pdf snapshot
    If the pdf file doesn't exist yet, it will save it

    Parameters
    ----------
    expected_filepath : str
        The file path to the expected pdf file
    actual_filepath: str
        The file path to the actual pdf file (must be different than expected_filepath)
    max_diff_val: num
        The max. value the difference between any pages, from 0-100
    """

    if not path.exists(actual_filepath):
        raise ValueError(f"Actual file {actual_filepath} doesn't exist")

    if not path.exists(expected_filepath):
        os.makedirs(os.path.dirname(expected_filepath), exist_ok=True)
        shutil.copy(actual_filepath, expected_filepath)
    else:
        # Get num pages for each pdf
        expected_num_pages = pypdftk.get_num_pages(expected_filepath)
        actual_num_pages = pypdftk.get_num_pages(actual_filepath)

        if expected_num_pages != actual_num_pages:
            raise ValueError(
                f"Expected {expected_num_pages} num pages; got {actual_num_pages} pages"
            )

        # Create temp dirs for each pdf
        try:
            expected_split_dir = tempfile.TemporaryDirectory()
            actual_split_dir = tempfile.TemporaryDirectory()

            # Split the pdf into different pages
            exp_split_files = pypdftk.split(expected_filepath, expected_split_dir.name)[
                1:
            ]
            act_split_files = pypdftk.split(actual_filepath, actual_split_dir.name)[1:]

            # Compare each page
            has_diff = False
            for page_idx in range(len(exp_split_files)):
                with Image(filename=exp_split_files[page_idx]) as expected_page:
                    with Image(filename=act_split_files[page_idx]) as actual_page:
                        expected_page.fuzz = 0.25 * expected_page.quantum_range
                        expected_page.artifacts["compare:highlight-color"] = "red"
                        expected_page.artifacts[
                            "compare:lowlight-color"
                        ] = "transparent"
                        diff_img, diff_val = expected_page.compare(
                            actual_page, "root_mean_square"
                        )

                        if diff_val > max_diff_val:
                            diff_img_filepath = os.path.join(
                                os.path.dirname(expected_filepath),
                                f"{os.path.basename(expected_filepath)}-{page_idx}-diff.jpg",
                            )
                            diff_img.save(filename=diff_img_filepath)
                            has_diff = True

                        diff_img.close()

            if has_diff:
                print("One or more pages in the pdf is different")
                print(f"See folder in {os.path.dirname(expected_filepath)} for diff")
                raise ValueError()
        finally:
            # Clean up the dirs
            expected_split_dir.cleanup()
            actual_split_dir.cleanup()
