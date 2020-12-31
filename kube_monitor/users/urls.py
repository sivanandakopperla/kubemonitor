from django.conf.urls import include, url
from django.urls import path
from rest_framework import routers
from users.views import *
from rest_framework_jwt.views import obtain_jwt_token

router = routers.SimpleRouter()
router.register(r'users_info', UserViewSet, basename="Users")
# urlpatterns = [
#     path('login/', obtain_jwt_token),
# ]
urlpatterns = router.urls