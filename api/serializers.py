from rest_framework import serializers
from .models import Video

class VideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Video
        fields = ['url', 'keywords', 'human_presence', 'visibility']
        extra_kwargs = {
            'visibility': {'required': False},  # Since visibility is optional
            'human_presence': {'required': False},  # Since human_presence is optional
            'keywords': {'required': False}  # Since keywords is optional
        }

    def validate_visibility(self, value):
        """
        Check that visibility is provided when human_presence is 'Single'.
        """
        data = self.initial_data
        if data['human_presence'] == 'S' and not value:
            raise serializers.ValidationError("Visibility must be set when human presence is 'Single'.")
        return value
