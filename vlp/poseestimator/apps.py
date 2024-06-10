from django.apps import AppConfig
from server.settings import BASE_DIR
import logging
import os
from mmengine.config.utils import MODULE2PACKAGE
from mmengine.utils import get_installed_path

mmpose_path = get_installed_path(MODULE2PACKAGE['mmpose'])
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


        # Do not touch anything here, it works as is haha
        mmpose_model_dir = f"{BASE_DIR}/poseestimator/mmpose-models"
        det_weights_path = f"{mmpose_model_dir}/rtmdet_m_8xb32-100e_coco-obj365-person-235e8209.pth"
        pose2d_weights_path = f"{mmpose_model_dir}/rtmpose-l_simcc-body7_pt-body7_420e-384x288-3f5a1437_20230504.pth"
        
        pose_inferencer = MMPoseInferencer(pose2d='rtmpose-l', pose2d_weights=pose2d_weights_path, det_model = os.path.join(
            mmpose_path, '.mim', 'demo/mmdetection_cfg/rtmdet_m_640-8xb32_coco-person.py'), det_weights=det_weights_path, det_cat_ids=(0, ))
