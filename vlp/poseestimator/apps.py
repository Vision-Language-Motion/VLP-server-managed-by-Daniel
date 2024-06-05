from django.apps import AppConfig
from server.settings import BASE_DIR
import logging
logger = logging.getLogger(__name__)

class PoseestimatorConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'poseestimator'

    def ready(self):
        # Import and initialize MMPoseInferencer here
        from mmpose.apis import MMPoseInferencer
        global pose_inferencer
        # You can now use MMPoseInferencer, e.g., initialize it
        # pose_inferencer = MMPoseInferencer('rtmpose-l')

        mmpose_model_dir = f"{BASE_DIR}/poseestimator/mmpose-models"
        pose2d = f"{mmpose_model_dir}/rtmdet_m_8xb32-100e_coco-obj365-person-235e8209.pth"
        pose2d_weights_path = f"{mmpose_model_dir}/rtmpose-l_simcc-body7_pt-body7_420e-384x288-3f5a1437_20230504.pth"
        
        logger.warn(f"pose2d: {pose2d}")
        pose_inferencer = MMPoseInferencer(pose2d='rtmpose-l', pose2d_weights=pose2d_weights_path, det_model="whole_image", det_weights=pose2d)

        # other things