from rest_framework import serializers
from server_stats.models import ServerStats


class ServerStatsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServerStats
        fields = ('server','disk_info','up_time','memory_info')