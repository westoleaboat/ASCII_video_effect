"""
ASCII Art Video Converter

### How to Run:
    $ python3 main.py --video /path/to/video.mp4 --output_folder /path/to/folder --cols 120 --fps 10 --scale 0.55 --more_levels

### Test:
    $ python -m unittest discover -s tests

### Profiling line by line (for optimization)

    - uncomment imports
    - add decorator @line_profiler.profile to the function you want to analyze.
    
    - option 1: Add LINE_PROFILE=1 and run script as normal.
        $ LINE_PROFILE=1 python3 main.py --video /path/to/video.mp4 --output_folder /path/to/folder --cols 120 --fps 10 --scale 0.55 --more_levels

    - option 2: The kernprof.py script will produce an output file and print the result of the profiling on the standard output.
        $ kernprof -l -v main.py --video /path/to/video.mp4 --output_folder /path/to/folder --cols 120 --fps 10 --scale 0.55 --more_levels

    To view details run:
    python -m line_profiler -rtmz main.py.lprof
"""

import os
import sys
import cv2
import argparse
from PIL import Image, ImageDraw, ImageFont
import numpy as np
from datetime import timedelta

# import line_profiler                  
# from line_profiler import profile

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
    print(f"Frames extracted to {output_folder}\n")

def getAverageL(image):
    """Return average brightness value of an image."""
    return np.mean(image)

# @line_profiler.profile
def frame_to_ascii(image, cols, scale, more_levels):
    """Convert a single frame to ASCII."""
    font = ImageFont.load_default()
    char_width, char_height = font.getbbox("A")[2], font.getbbox("A")[3]

    # Convert to grayscale
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    H, W = image.shape

    # Compute tile dimensions
    tile_width = W / cols
    tile_height = tile_width / scale
    rows = int(H / tile_height)

    # Check for invalid cols or rows
    if cols > W or rows > H:
        raise ValueError("Image resolution is too low for the specified cols.")

    # Pre-compute brightness to ASCII mapping
    scale_map = gscale1 if more_levels else gscale2
    brightness_to_char = np.array([scale_map[min(int((i * len(scale_map)) / 255), len(scale_map) - 1)] for i in range(256)])

    # Create grid for tiles
    tile_rows = np.linspace(0, H, rows + 1, dtype=int)
    tile_cols = np.linspace(0, W, cols + 1, dtype=int)

    # Calculate brightness for each tile in bulk
    ascii_image = []
    for j in range(rows):
        row_tiles = [
            brightness_to_char[int(image[tile_rows[j]:tile_rows[j + 1], tile_cols[i]:tile_cols[i + 1]].mean())]
            for i in range(cols)
        ]
        ascii_image.append("".join(row_tiles))

    # Convert ASCII art back to an image
    img_width = char_width * cols
    img_height = char_height * rows
    ascii_img = Image.new("L", (img_width, img_height), 255)
    draw = ImageDraw.Draw(ascii_img)

    for j, row in enumerate(ascii_image):
        draw.text((0, j * char_height), row, fill=0, font=font)

    return ascii_img


# @line_profiler.profile
def apply_ascii_effect(input_folder, output_folder, cols=120, scale=0.5, more_levels=False):
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
        print(f"\rProcessing frame {index + 1}/{len(files)}: {filename}", end="")

        # Load and process image
        image = cv2.imread(os.path.join(input_folder, filename))
        ascii_img = frame_to_ascii(image, cols, scale, more_levels)

        # Save ASCII frame as an image
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

