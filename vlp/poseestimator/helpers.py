import logging
logger = logging.getLogger(__name__)
import os
from server.settings import BASE_DIR




#def get_pose_inference(filepath="poseestimator/800Kräfte_auf_skifahrer_am_hang.jpeg"):
def get_pose_inference(filepath="poseestimator/MenschenNebeneinander.jpg"):
    """Uses MMPose to infer poses from an image. Result format
    
    dictionary with keys:
    visualization': None, 
    'predictions': [[{
        'keypoints': [[535.6224365234375, 204.6596221923828], ...], 
        'keypoint_scores': [0.9561091065406799, 1.0398149490356445, ...],
        'bbox': ([97.65226745605469, 94.52516174316406, 584.6615600585938, 486.0082702636719],),
        'bbox_score': 0.9103934
    """
    from .apps import pose_inferencer
    logger.warn("In get_pose_inference")

    vis_out_path = os.path.join(BASE_DIR, "poseestimator/predictions")
    logger.warn(f"In get_pose_inference 2 {filepath}")

    result_generator = pose_inferencer(filepath, pred_out_dir=os.path.join(BASE_DIR, "poseestimator/predictions"))
    logger.warn(result_generator)
    result = next(result_generator)

    logger.warn("In get_pose_inference 3")


    logger.warn(result)
    return result
    

def check_keypoint_visibility(keypoints) -> bool:
    """At least 5 keypoints should be visible
    a head-keypoint (1-5) must have a score of more than 0.7 to be
    considered visible,
    a body-keypoint (6-17) must have a score of more than 0.35 to be
    considered visible
    """

    head_keypoints = keypoints[:5]
    body_keypoints = keypoints[5:]
    head_visible = sum([1 for score in head_keypoints if score > 0.7])
    body_visible = sum([1 for score in body_keypoints if score > 0.35])
    visible_keypoint_count = head_visible + body_visible
    
    return visible_keypoint_count >= 5


def check_bbox_score(bbox_score) -> bool:
    """The bounding box score should be more than 0.4"""
    return bbox_score > 0.4


def get_bbox_area_ratio(bbox, frame_area) -> bool:
    """The bounding box area should be more than 1/60 of the frame area"""
    bbox_area = (bbox[2] - bbox[0]) * (bbox[3] - bbox[1])
    return bbox_area/frame_area



def max_shoulder_score(keypoints):
    return max(keypoints[5], keypoints[6])

def max_knee_score(keypoints):
    return max(keypoints[13], keypoints[14])

def three_keypoints_among_shoulders_elbows_hands_visible(keypoints):
    return sum([1 for i in [5, 6, 7, 8, 9, 10] if keypoints[i] > 0.5]) >= 3