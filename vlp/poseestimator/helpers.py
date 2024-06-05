import logging
logger = logging.getLogger(__name__)
import os
from server.settings import BASE_DIR

#def get_pose_inference(filepath="poseestimator/800Kräfte_auf_skifahrer_am_hang.jpeg"):
def get_pose_inference(filepath="poseestimator/MenschenNebeneinander.jpg"):
    """Uses MMPose to infer poses from an image. Result format
    
    dictionary with keys:
    visualization': None, 
    'predictions': [[{'keypoints': [[535.6224365234375, 204.6596221923828], ...], 
    'keypoint_scores': [0.9561091065406799, 1.0398149490356445, ...],
    'bbox': ([97.65226745605469, 94.52516174316406, 584.6615600585938, 486.0082702636719],),
    'bbox_score': 0.9103934
    """
    from .apps import pose_inferencer


    vis_out_path = os.path.join(BASE_DIR, "poseestimator/predictions")

    result_generator = pose_inferencer(filepath, pred_out_dir=os.path.join(BASE_DIR, "poseestimator/predictions"), vis_out_dir=vis_out_path, draw_bbox=True)
    result = next(result_generator)



    logger.warn(result)
    return result
    
