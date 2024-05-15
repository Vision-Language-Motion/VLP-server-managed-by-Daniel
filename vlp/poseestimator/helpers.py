import logging
logger = logging.getLogger(__name__)

def get_pose_inference():
    from .apps import pose_inferencer

    result_generator = pose_inferencer("poseestimator/800Kräfte_auf_skifahrer_am_hang.jpeg")
    result = next(result_generator)

    logger.warn(result)

    
