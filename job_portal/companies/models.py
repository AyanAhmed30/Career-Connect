from django.db import models
from django.conf import settings  # Import settings
from django.contrib.auth import get_user_model

User = get_user_model()

class Job(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    company = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='jobs')  # Use AUTH_USER_MODEL
    required_skills = models.CharField(max_length=255, blank=True, null=True)
    experience = models.CharField(max_length=100, blank=True, null=True)
    qualifications = models.CharField(max_length=255, blank=True, null=True)
    age = models.PositiveIntegerField(blank=True, null=True)
    posted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
