from django.test import TestCase
import logging

class PoseInferenceTestCase(TestCase):
    def test_pose_inference_logging(self):
        from poseestimator.helpers import get_pose_inference
        get_pose_inference()
        
