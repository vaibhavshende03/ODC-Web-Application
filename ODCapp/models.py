from django.db import models

# Create your models here.

from django.contrib.auth.models import User

class DetectedObject(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    label = models.CharField(max_length=100)
    count = models.IntegerField()

    def __str__(self):
        return f"{self.label} ({self.count}) at {self.timestamp}"

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True)
    location = models.CharField(max_length=30, blank=True)
    birth_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.user.username