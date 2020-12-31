from django.conf.urls import include, url
from rest_framework import routers
from server_stats.views import ServerStatsViewSet


router = routers.SimpleRouter()
router.register(r'server_info', ServerStatsViewSet, basename="server_stats")

urlpatterns = router.urls