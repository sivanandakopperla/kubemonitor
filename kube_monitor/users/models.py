
from djongo import models
from django.contrib.auth.models import User


# Create your models here.
class UserRegister(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reg_user')
    mobile_no = models.CharField(max_length=255)
    hometown = models.CharField(max_length=255)
    date = models.DateTimeField(auto_now_add=True)
