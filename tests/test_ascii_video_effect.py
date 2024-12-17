import unittest
import os
import shutil
from ascii_video_effect import extract_frames, apply_ascii_effect, create_video_from_frames

class TestASCIIArtConverter(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Set up temporary directories and test assets."""
        cls.test_assets_dir = "tests/assets"
        cls.sample_video_path = os.path.join(cls.test_assets_dir, "sample_video.mp4")
        cls.temp_output_dir = "tests/temp_output"
        os.makedirs(cls.temp_output_dir, exist_ok=True)

    @classmethod
    def tearDownClass(cls):
        """Clean up temporary directories after tests."""
        if os.path.exists(cls.temp_output_dir):
            shutil.rmtree(cls.temp_output_dir)

    def test_extract_frames(self):
        """Test frame extraction."""
        temp_frames_dir = os.path.join(self.temp_output_dir, "frames")
        extract_frames(self.sample_video_path, temp_frames_dir, fps=1)
        
        # Check if frames are extracted
        self.assertTrue(os.path.exists(temp_frames_dir))
        extracted_frames = os.listdir(temp_frames_dir)
        self.assertGreater(len(extracted_frames), 0, "No frames were extracted.")
        self.assertTrue(extracted_frames[0].endswith(".jpg"), "Frames are not in the correct format.")

    def test_apply_ascii_effect(self):
        """Test ASCII effect application."""
        temp_frames_dir = os.path.join(self.temp_output_dir, "frames")
        temp_ascii_frames_dir = os.path.join(self.temp_output_dir, "ascii_frames")

        # Ensure frames are extracted first
        extract_frames(self.sample_video_path, temp_frames_dir, fps=1)
        apply_ascii_effect(temp_frames_dir, temp_ascii_frames_dir, cols=120, scale=0.5, more_levels=False)

        # Check if ASCII frames are created
        self.assertTrue(os.path.exists(temp_ascii_frames_dir))
        ascii_frames = os.listdir(temp_ascii_frames_dir)
        self.assertGreater(len(ascii_frames), 0, "No ASCII frames were generated.")
        self.assertTrue(ascii_frames[0].endswith(".png"), "ASCII frames are not in the correct format.")

    def test_create_video_from_frames(self):
        """Test video reconstruction from frames."""
        temp_frames_dir = os.path.join(self.temp_output_dir, "frames")
        temp_ascii_frames_dir = os.path.join(self.temp_output_dir, "ascii_frames")
        output_video_path = os.path.join(self.temp_output_dir, "ascii_video.mp4")

        # Ensure ASCII frames are generated
        extract_frames(self.sample_video_path, temp_frames_dir, fps=1)
        apply_ascii_effect(temp_frames_dir, temp_ascii_frames_dir, cols=120, scale=0.5, more_levels=False)
        create_video_from_frames(temp_ascii_frames_dir, output_video_path, fps=1)

        # Check if the output video exists
        self.assertTrue(os.path.exists(output_video_path), "Output video was not created.")
        self.assertTrue(output_video_path.endswith(".mp4"), "Output video is not in the correct format.")

if __name__ == "__main__":
    unittest.main()
