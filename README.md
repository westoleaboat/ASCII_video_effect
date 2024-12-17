<<<<<<< HEAD
# ASCII_video_effect
processes a video file to generate an ASCII art-styled version of the video. 
=======
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


### Notes:
- The script creates temporary folders for storing intermediate frames and ASCII-converted frames.
- Adjust the `cols` and `scale` parameters to control the resolution of the ASCII art. (higher cols = longer rendering time)
>>>>>>> de8acc0 ((ADD) main file, gif, update Readme)
