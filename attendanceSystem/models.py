from django.contrib.auth.models import User
from django.db import models


class Attendance(models.Model):
    rollNo = models.CharField(max_length=11, default="")
    date = models.CharField(max_length=11)

    def __int__(self):
        return self.id
