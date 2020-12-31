from django.shortcuts import render
from rest_framework import viewsets
from server_stats.serializers import ServerStatsSerializer
from server_stats.controllers import ServerStatsController
from django.http import HttpResponse
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
# Create your views here.


class ServerStatsViewSet(viewsets.ModelViewSet, ServerStatsController):
    '''
    API endpoint that allows to get general information about Servers.
    '''
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)
    serializer_class = ServerStatsSerializer

    def create(self, request, *args, **kwargs):
        return HttpResponse(self.update_stats(request))

    def update(self, request, pk=None):
        return HttpResponse(self.update_stats_specific(request, pk))

    def list(self, request, *args, **kwargs):
        return HttpResponse(self.get_stats_info_list(request))

    def retrieve(self, request, pk=None):
        return HttpResponse(self.get_stats_info(request, pk))

    def destroy(self, request, pk=None):
        return HttpResponse(self.stats_delete(request, pk))