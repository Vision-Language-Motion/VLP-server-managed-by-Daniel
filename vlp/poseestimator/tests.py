from django.test import TestCase
import logging
import tempfile
from .hanposealgorithm import process_video

class PoseInferenceTestCase(TestCase):
    def test_pose_inference_logging(self):
        from poseestimator.helpers import get_pose_inference
        get_pose_inference()

        
# When testing remove the hashtag in line 133 of hanposealgorithm
class HansPyScene(TestCase):
    def test_process_video(self):
        with tempfile.TemporaryDirectory() as temp_output_dir:
            test_video_path = 'poseestimator/test_video/car.mp4'
            results = process_video(test_video_path, temp_output_dir)
            for result in results:
                print(f"Video Name: {result[0]}, Start Time: {result[1]:.2f}s, End Time: {result[2]:.2f}s, Classification: {result[3]}")
