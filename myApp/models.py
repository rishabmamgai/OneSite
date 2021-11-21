from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    branch = models.CharField(max_length=50, default="")
    batch = models.CharField(max_length=12, default="")
    contact = models.CharField(max_length=15, default="")


class Sem1(models.Model):
    roll_no = models.IntegerField()
    mid_sem = models.TextField()
    end_sem = models.TextField(default="")
    practicals = models.TextField(default="")


class Sem2(models.Model):
    roll_no = models.IntegerField()
    mid_sem = models.TextField()
    end_sem = models.TextField(default="")
    practicals = models.TextField(default="")


class Sem3(models.Model):
    roll_no = models.IntegerField()
    mid_sem = models.TextField()
    end_sem = models.TextField(default="")
    practicals = models.TextField(default="")


class Sem4(models.Model):
    roll_no = models.IntegerField()
    mid_sem = models.TextField()
    end_sem = models.TextField(default="")
    practicals = models.TextField(default="")


class Sem5(models.Model):
    roll_no = models.IntegerField()
    mid_sem = models.TextField()
    end_sem = models.TextField(default="")
    practicals = models.TextField(default="")


class Sem6(models.Model):
    roll_no = models.IntegerField()
    mid_sem = models.TextField()
    end_sem = models.TextField(default="")
    practicals = models.TextField(default="")


class Sem7(models.Model):
    roll_no = models.IntegerField()
    mid_sem = models.TextField()
    end_sem = models.TextField(default="")
    practicals = models.TextField(default="")


class Sem8(models.Model):
    roll_no = models.IntegerField()
    mid_sem = models.TextField()
    end_sem = models.TextField(default="")
    practicals = models.TextField(default="")
