from django.urls import include, path
from rest_framework import routers

from api import views

router = routers.DefaultRouter()
router.register(r'videos', views.VideoViewSet)

# (commented out) Wire up our API using automatic URL routing.
# (commented out) Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('', include(router.urls)),
#     path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]