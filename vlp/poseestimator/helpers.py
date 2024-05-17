import logging
logger = logging.getLogger(__name__)

def get_pose_inference(filepath="poseestimator/800Kräfte_auf_skifahrer_am_hang.jpeg"):
    from .apps import pose_inferencer

    result_generator = pose_inferencer(filepath)
    result = next(result_generator)

    logger.warn(result)

    
