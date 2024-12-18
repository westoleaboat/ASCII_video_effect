import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import time

# Grayscale scales
gscale1 = "$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/|()1{}[]?-_+~<>i!lI;:,\"^`'. "
gscale2 = '@%#*+=-:. '

def get_average_l(image):
    """Calculate the average brightness of an image."""
    im = np.array(image)
    return np.average(im)

def frame_to_ascii(image, cols=120, scale=0.5, more_levels=False):
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

    # Create ASCII art
    ascii_image = []
    for j in range(rows):
        y1 = int(j * tile_height)
        y2 = int((j + 1) * tile_height) if j != rows - 1 else H
        ascii_image.append("")
        for i in range(cols):
            x1 = int(i * tile_width)
            x2 = int((i + 1) * tile_width) if i != cols - 1 else W
            tile = image[y1:y2, x1:x2]
            avg = int(get_average_l(tile))
            gsval = gscale1[min(int((avg * 69) / 255), len(gscale1) - 1)] if more_levels else \
                    gscale2[min(int((avg * 9) / 255), len(gscale2) - 1)]
            ascii_image[j] += gsval

    # Convert ASCII art back to an image
    img_width = char_width * cols
    img_height = char_height * rows
    ascii_img = Image.new("L", (img_width, img_height), 255)
    draw = ImageDraw.Draw(ascii_img)

    for j, row in enumerate(ascii_image):
        draw.text((0, j * char_height), row, fill=0, font=font)

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
    scale = 0.8
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
