#Django lib
from django.shortcuts import render
from rest_framework import viewsets
from users.serializers import UserSerializer, UserRegisterSerializer
from users.controllers import UserController
from django.http import HttpResponse
import pdb
import json
from rest_framework import views
from rest_framework.response import Response
from django.contrib.auth.models import User
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly


# Create your views here.
class UserViewSet(viewsets.ModelViewSet, UserController):
    '''
    API endpoint that allows to get users information.
    '''

    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)
    serializer_class = UserSerializer

    def list(self, request, *args, **kwargs):
        return HttpResponse(self.get_user_info_list(request))

    def retrieve(self, request, pk=None):
        return HttpResponse(self.get_user_info(request, pk))

    def create(self, request, *args, **kwargs):
        return HttpResponse(self.register(request))

    def update(self, request, pk=None):
        return HttpResponse(self.user_update(request, pk))

    def destroy(self, request, pk=None):
        return HttpResponse(self.user_delete(request, pk))