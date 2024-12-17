"""
ASCII Art Video Converter

### How to Run:
    $ python3 ascii_video_effect.py --video /path/to/video.mp4 --output_folder /path/to/folder --cols 120 --fps 10 --scale 0.55 --more_levels

### Test:
    $ python -m unittest discover -s tests

"""


import os
import sys
import cv2
import argparse
from PIL import Image, ImageDraw, ImageFont
import numpy as np
from datetime import timedelta

# Grayscale scales
gscale1 = "$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/|()1{}[]?-_+~<>i!lI;:,\"^`'. "
gscale2 = '@%#*+=-:. '

def format_timedelta(td):
    """Format timedelta to a string suitable for filenames."""
    result = str(td)
    try:
        result, ms = result.split(".")
    except ValueError:
        return (result + ".00").replace(":", "-")
    ms = int(ms)
    ms = round(ms / 1e4)
    return f"{result}.{ms:02}".replace(":", "-")

def get_saving_frames_durations(cap, saving_fps):
    """Return a list of timestamps to save frames."""
    s = []
    clip_duration = cap.get(cv2.CAP_PROP_FRAME_COUNT) / cap.get(cv2.CAP_PROP_FPS)
    for i in np.arange(0, clip_duration, 1 / saving_fps):
        s.append(i)
    return s

def extract_frames(video_path, output_folder, fps):
    """Extract frames from the video."""
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    cap = cv2.VideoCapture(video_path)
    saving_frames_durations = get_saving_frames_durations(cap, fps)
    count = 0
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    print(f"Extracting {frame_count} frames...")

    while True:
        is_read, frame = cap.read()
        if not is_read:
            break

        frame_duration = count / cap.get(cv2.CAP_PROP_FPS)
        if saving_frames_durations and frame_duration >= saving_frames_durations[0]:
            frame_duration_formatted = format_timedelta(timedelta(seconds=frame_duration))
            frame_filename = os.path.join(output_folder, f"frame{frame_duration_formatted}.jpg")
            cv2.imwrite(frame_filename, frame)
            saving_frames_durations.pop(0)

        count += 1

    cap.release()
    print(f"Frames extracted to {output_folder}")

def getAverageL(image):
    """Return average brightness value of an image."""
    im = np.array(image)
    return np.average(im)

def apply_ascii_effect(input_folder, output_folder, cols, scale, more_levels):
    """Apply ASCII effect to all frames in the input folder."""
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    files = sorted(
        [f for f in os.listdir(input_folder) if f.endswith(".jpg") or f.endswith(".png")],
        key=lambda x: int("".join(filter(str.isdigit, x)) or 0)
    )

    font = ImageFont.load_default()
    char_width, char_height = font.getbbox("A")[2], font.getbbox("A")[3]

    for index, filename in enumerate(files):
        print(f"\rApplying ASCII effect to frame {index + 1}/{len(files)}: {filename}", end="")
        image = Image.open(os.path.join(input_folder, filename)).convert('L')
        W, H = image.size
        w = W / cols
        h = w / scale
        rows = int(H / h)

        if cols > W or rows > H:
            print(f"Frame {filename} too small for the specified cols.")
            continue

        aimg = []
        for j in range(rows):
            y1 = int(j * h)
            y2 = int((j + 1) * h) if j != rows - 1 else H
            aimg.append("")
            for i in range(cols):
                x1 = int(i * w)
                x2 = int((i + 1) * w) if i != cols - 1 else W
                img = image.crop((x1, y1, x2, y2))
                avg = int(getAverageL(img))
                # gsval = gscale1[int((avg * 69) / 255)] if more_levels else gscale2[int((avg * 9) / 255)]
                gsval = gscale1[min(int((avg * 69) / 255), len(gscale1) - 1)] if more_levels else gscale2[min(int((avg * 9) / 255), len(gscale2) - 1)]
                aimg[j] += gsval

        img_width = char_width * cols
        img_height = char_height * rows
        ascii_img = Image.new("L", (img_width, img_height), 255)
        draw = ImageDraw.Draw(ascii_img)

        for j, row in enumerate(aimg):
            draw.text((0, j * char_height), row, fill=0, font=font)

        output_path = os.path.join(output_folder, f"ascii_frame_{index + 1:04d}.png")
        ascii_img.save(output_path)
    print("\nASCII effect applied to all frames.")

def create_video_from_frames(input_folder, output_path, fps):
    """Create a video from frames."""
    images = sorted(
        [img for img in os.listdir(input_folder) if img.endswith((".png", ".jpg"))],
        key=lambda x: int("".join(filter(str.isdigit, x)) or 0)
    )

    if not images:
        print("No frames found in the input folder.")
        return

    first_frame = cv2.imread(os.path.join(input_folder, images[0]))
    height, width, layers = first_frame.shape
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    video = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

    print(f"Creating video at {output_path}...")
    for idx, image_name in enumerate(images):
        frame = cv2.imread(os.path.join(input_folder, image_name))
        video.write(frame)
        print(f"\rProcessing frame {idx + 1}/{len(images)}: {image_name}", end="")

    video.release()
    print(f"\nVideo saved at {output_path}")

def main():
    '''    
    This script processes a video file to generate an ASCII art-styled version of the video. 
    It performs the following steps sequentially:

    1. Extract Frames:
        - The input video is split into individual frames and saved in a temporary folder.

    2. Apply ASCII Effect:
        - Each extracted frame is converted to an ASCII art image using a grayscale character map. 
        - The ASCII effect is applied by mapping pixel intensity values to characters in the map.

    3. Reconstruct Video:
        - The ASCII-processed frames are combined to create a new video with the same frame rate as the original.
    '''

    parser = argparse.ArgumentParser(
        description="Convert a video into an ASCII art-styled video.",
        epilog="Example: python3 complete.py --video input.mp4 --output_folder output --cols 150 --scale 0.4 --fps 24 --more_levels"
    )

    parser.add_argument("--video", required=True, help="Path to the input video file.")
    parser.add_argument("--output_folder", required=True, help="Folder to save the final ASCII video.")
    parser.add_argument("--cols", type=int, default=120, help="Number of ASCII characters per row. Default is 120.")
    parser.add_argument("--scale", type=float, default=0.5, help="Aspect ratio for ASCII art. Default is 0.5.")
    parser.add_argument("--fps", type=int, help="Frames per second for the output video. Defaults to input video's FPS.")
    parser.add_argument("--more_levels", action="store_true", help="Use a more detailed grayscale map for higher fidelity.")

    # Check if no arguments are provided
    if len(sys.argv) == 1:
        parser.print_help(sys.stderr)
        sys.exit(1)

    args = parser.parse_args()

    # Call main processing logic
    process_video(args)

def process_video(args):
    print("Processing video...")
    
    temp_frame_folder = os.path.join(args.output_folder, "frames")
    temp_ascii_folder = os.path.join(args.output_folder, "ascii_frames")
    final_video_path = os.path.join(args.output_folder, "ascii_video.mp4")

    # Step 1: Extract frames
    extract_frames(args.video, temp_frame_folder, args.fps)

    # Step 2: Apply ASCII effect
    apply_ascii_effect(temp_frame_folder, temp_ascii_folder, args.cols, args.scale, args.more_levels)

    # Step 3: Create final video
    create_video_from_frames(temp_ascii_folder, final_video_path, args.fps)

if __name__ == "__main__":
    main()

