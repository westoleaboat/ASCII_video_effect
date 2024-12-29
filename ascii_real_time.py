import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import time

# Grayscale scales
gscale1 = "$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/|()1{}[]?-_+~<>i!lI;:,\"^`'. "
gscale2 = "@%#*+=-:. "

def frame_to_ascii(image, cols=90, scale=0.4, more_levels=False):
    """Convert a single frame to ASCII."""
    font = ImageFont.load_default()
    char_width, char_height = font.getbbox("A")[2], font.getbbox("A")[3]

    # Convert to grayscale
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    H, W = image.shape

    # Compute tile width and height
    tile_width = W / cols
    tile_height = tile_width / scale
    rows = int(H / tile_height)

    # Check for invalid cols or rows
    if cols > W or rows > H:
        raise ValueError("Image resolution is too low for the specified cols.")

    # Reshape image into tiles
    tile_rows = np.linspace(0, H, rows + 1, dtype=int)
    tile_cols = np.linspace(0, W, cols + 1, dtype=int)

    # Calculate brightness for each tile
    brightness = np.zeros((rows, cols), dtype=np.float32)
    for j in range(rows):
        for i in range(cols):
            tile = image[tile_rows[j]:tile_rows[j + 1], tile_cols[i]:tile_cols[i + 1]]
            brightness[j, i] = tile.mean()

    # Map brightness to ASCII characters
    scale_map = gscale1 if more_levels else gscale2
    char_map = np.vectorize(lambda x: scale_map[min(int((x * len(scale_map)) / 255), len(scale_map) - 1)])
    ascii_array = char_map(brightness)

    # Convert ASCII art back to an image
    img_width = char_width * cols
    img_height = char_height * rows
    ascii_img = Image.new("L", (img_width, img_height), 255)
    draw = ImageDraw.Draw(ascii_img)

    for j, row in enumerate(ascii_array):
        draw.text((0, j * char_height), "".join(row), fill=0, font=font)

    return np.array(ascii_img)

def main():
    """Run the real-time ASCII art effect on webcam feed."""
    # Initialize webcam feed
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error: Cannot access webcam.")
        return

    # Set desired output resolution (adjust for performance)
    cols = 90
    scale = 0.4
    more_levels = False

    print("Press 'q' to quit.")
    fps_list = []

    while True:
        start_time = time.time()
        
        ret, frame = cap.read()
        if not ret:
            print("Failed to grab frame.")
            break

        try:
            # Apply ASCII effect to frame
            ascii_frame = frame_to_ascii(frame, cols=cols, scale=scale, more_levels=more_levels)
        except ValueError as e:
            print(e)
            break

        # Resize ASCII image to fit the screen
        ascii_frame = cv2.resize(ascii_frame, (frame.shape[1], frame.shape[0]))

        # Show ASCII frame
        cv2.imshow("ASCII Art Webcam", ascii_frame)

        # Calculate and display FPS
        elapsed_time = time.time() - start_time
        fps = 1 / elapsed_time
        fps_list.append(fps)
        avg_fps = sum(fps_list[-30:]) / min(len(fps_list), 30)
        print(f"\rFPS: {fps:.2f} (Average: {avg_fps:.2f})", end="")

        # Exit on 'q'
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    print("\nWebcam closed.")

if __name__ == "__main__":
    main()
