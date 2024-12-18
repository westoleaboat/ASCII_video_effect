
```
         _    ___     __              ___   _____ ______________   ___         __ 
        | |  / (_)___/ /__  ____     /   | / ___// ____/  _/  _/  /   |  _____/ /_
        | | / / / __  / _ \/ __ \   / /| | \__ \/ /    / / / /   / /| | / ___/ __/
        | |/ / / /_/ /  __/ /_/ /  / ___ |___/ / /____/ /_/ /   / ___ |/ /  / /_  
        |___/_/\__,_/\___/\____/  /_/  |_/____/\____/___/___/  /_/  |_/_/   \__/  
                                                                    
                    ┏┓┏┓┏┓┳┳             ┓   ┓         •        ┏            ┏           
   ┏┓┏┓┏┓┏┓┏┓┏┓╋┏┓  ┣┫┗┓┃ ┃┃  ┏┓┏┓╋━━┏╋┓┏┃┏┓┏┫  ┓┏┏┓┏┓┏┓┏┓┏┓  ┏┓╋  ┓┏┏┓┓┏┏┓  ╋┏┓┏┓┏┳┓┏┓┏ 
   ┗┫┗ ┛┗┗ ┛ ┗┻┗┗   ┛┗┗┛┗┛┻┻  ┗┻┛ ┗  ┛┗┗┫┗┗ ┗┻  ┗┛┗ ┛ ┛┗┗┛┛┗  ┗┛┛  ┗┫┗┛┗┻┛   ┛┛ ┗┻┛┗┗┗ ┛•
    ┛                                   ┛                           ┛                    

```

![sample](torus5.gif)

### How to Run:
    $ python main.py --video /path/to/video.mp4 --output_folder /path/to/folder --cols 120 --fps 10 --scale 0.55 --more_levels



    --video:            The path to the input video file (required).
    --output_folder:    The path to the folder where the final ASCII video will be saved (required).
    --cols:             The number of ASCII characters per row in the output (default: 120).
    --scale:            The aspect ratio for the ASCII art (default: 0.5).
    --fps:              Frames per second for the output video (default: inferred from the input video).
    --more_levels:      Use a detailed grayscale map for higher fidelity (default: False).

### Requirements:
    $ pip install -r requirements.txt


### Test:
    $ python -m unittest discover -s tests


### Notes:
- The script creates temporary folders for storing intermediate frames and ASCII-converted frames.
- Adjust the `cols` and `scale` parameters to control the resolution of the ASCII art. (higher cols = longer rendering time)
- At low `cols` value the result improves removing `more_levels` flag

### Real-time webcam processing:

To use this effect with your webcam feed run:
```
$ python ascii_real_time.py
```
![real_feed](live_feed.gif)

### Improve
1. Robust Error Handling
    - Detect Issues with Input Video:
        - [ ] Validate the input video path and format.
        - [ ] Check if the video file is corrupt or unreadable.
        - [ ] Handle cases where input video has zero frames or unsupported codec.

    - Output Folder Handling: 
        - [ ] Warn if the output folder exists to avoid overwriting files.
        - [ ] Create subditrectories dynamically if necessary.

    - Resource Cleanup:
        - [ ] Ensure temp folders and files are deleted after processing, even if errors when running.

2. Improve Performance
    - [ ] Parallel Processing
    - [ ] Batch File I/O
    - [ ] GPU Acceleration

3. Customization 
    - [ ] Dynamic Resolution Scaling: adjust `cols` and `scale` based on resolution of the input video.
    - [ ] Aspect Ratio Correction: handle input videos with non-standard aspect ratios (e.g., cropping or padding).

