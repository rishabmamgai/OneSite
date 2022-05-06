from django.contrib.auth.models import Group
from django.db import models
import os


class Assignment(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    topic = models.CharField(max_length=300)
    dueDate = models.DateTimeField(blank=True, null=True)
    description = models.TextField(blank=True)
    file = models.FileField(upload_to='communicationSystem/assignments', blank=True)


class Submission(models.Model):
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE)
    submittedBy = models.CharField(max_length=11)
    submission = models.FileField(upload_to='communicationSystem/assignmentsSubmitted', blank=False)
    submissionDate = models.DateTimeField(auto_now=True)

    def filename(self):
        return os.path.basename(self.submission.name)
