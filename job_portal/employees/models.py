# models.py
from django.db import models
from django.conf import settings
from companies.models import Job

class AppliedJob(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    resume = models.FileField(upload_to='resumes/', null=True, blank=True)
    status = models.CharField(max_length=50, default='Pending')
    
    # New fields for interview details
    interview_date = models.DateField(null=True, blank=True)
    interview_time = models.TimeField(null=True, blank=True)
    interview_location = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} applied for {self.job.title}"
