from djongo import models
from django_prometheus.models import ExportModelOperationsMixin

#Create your models here.


class ServerStats(ExportModelOperationsMixin('server'), models.Model):
    server = models.CharField(max_length=255)

    # file_system = models.CharField(max_length=255)
    # total_size = models.CharField(max_length=255)
    # use_percentage = models.CharField(max_length=255)
    # free_space = models.CharField(max_length=255)
    # used_space = models.CharField(max_length=255)
    disk_info = models.JSONField()
    up_time = models.CharField(max_length=255)

    # available_memory = models.CharField(max_length=255)
    # cache_memory = models.CharField(max_length=255)
    # free_memory = models.CharField(max_length=255)
    # shared_memory = models.CharField(max_length=255)
    # total_memory = models.CharField(max_length=255)
    # used_memory = models.CharField(max_length=255)

    memory_info = models.JSONField()

    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'tbl_server_stats'