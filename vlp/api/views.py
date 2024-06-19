from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from .models import Video, Keyword
from .serializers import VideoSerializer, KeywordSerializer
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

class VideoViewSet(viewsets.ModelViewSet):
    queryset = Video.objects.all()
    serializer_class = VideoSerializer

    @method_decorator(csrf_exempt, name='dispatch')
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        serializer.save()

class KeywordViewSet(viewsets.ModelViewSet):
    queryset = Keyword.objects.all().order_by('queue_pos')
    serializer_class = KeywordSerializer

    