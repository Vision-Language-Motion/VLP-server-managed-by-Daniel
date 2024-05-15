from django.apps import AppConfig

class PoseestimatorConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'poseestimator'

    def ready(self):
        # Import and initialize MMPoseInferencer here
        from mmpose.apis import MMPoseInferencer
        global pose_inferencer
        # You can now use MMPoseInferencer, e.g., initialize it
        pose_inferencer = MMPoseInferencer('rtmpose-l')

        # other things