import glob
import os
import matplotlib.pyplot as plt
import cv2
from .video_segment_finder import VideoSegmentFinder


def plot_timestamps_vs_pixel_change(stats):
    simple_timestamp = {}

    for frame_num in stats:
        timestamp_ms = stats[frame_num]["timestamp"]
        timestamp_seconds = int(float(timestamp_ms) / 100)
        num_pixels_changed = stats[frame_num]["num_pixels_changed"]

        if timestamp_seconds not in simple_timestamp:
            simple_timestamp[timestamp_seconds] = [sys.maxsize, 0, 0, 0]

        simple_timestamp[timestamp_seconds] = [
            min(simple_timestamp[timestamp_seconds][0], num_pixels_changed),  # min
            max(simple_timestamp[timestamp_seconds][1], num_pixels_changed),  # max
            simple_timestamp[timestamp_seconds][2] + num_pixels_changed,  # avg
            simple_timestamp[timestamp_seconds][3] + 1,  # num points
        ]

    # Compute avg
    for k in simple_timestamp:
        simple_timestamp[k][2] /= simple_timestamp[k][3]

    x_vals = sorted(simple_timestamp.keys())

    plt.plot(x_vals, [simple_timestamp[x][0] for x in x_vals], label="min")
    plt.plot(x_vals, [simple_timestamp[x][1] for x in x_vals], label="max")
    plt.plot(x_vals, [simple_timestamp[x][2] for x in x_vals], label="avg")

    plt.xlabel("timestamp")
    plt.ylabel("score")

    plt.legend()
    plt.show()


def save_selected_frames(selected_frames):
    # Prepare the output folder
    if not os.path.exists("./plot-output"):
        os.mkdir("plot-output")
    for f in glob.glob("./plot-output/*"):
        os.remove(f)

    # Save the frames into the output folder
    for frame_num in selected_frames:
        timestamp = selected_frames[frame_num]["timestamp"]
        pixel_changes = selected_frames[frame_num]["num_pixels_changed"]
        frame = selected_frames[frame_num]["frame"]
        next_frame = selected_frames[frame_num]["next_frame"]
        mask = selected_frames[frame_num]["mask"]

        cv2.imwrite(
            "plot-output/{}_{}_cur_frame.jpeg".format(timestamp, pixel_changes), frame
        )
        cv2.imwrite(
            "plot-output/{}_{}_next_frame.jpeg".format(timestamp, pixel_changes),
            next_frame,
        )
        cv2.imwrite(
            "plot-output/{}_{}_mask_frame.jpeg".format(timestamp, pixel_changes), mask
        )


if __name__ == "__main__":
    selected_frames, stats = VideoSegmentFinder().get_segment_frames_with_stats(
        "./tests/videos/input_6.mp4"
    )
    save_selected_frames(selected_frames)
    plot_timestamps_vs_pixel_change(stats)
