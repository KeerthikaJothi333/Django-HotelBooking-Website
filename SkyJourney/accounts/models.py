from django.db import models


# Create your models here.
from django.utils import timezone
from datetime import timedelta

class EmailOTP(models.Model):
    email = models.EmailField()
    otp = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)

    def is_expired(self):
        return timezone.now() > self.created_at + timedelta(minutes=10)

    def __str__(self):
        return f"{self.email} - {self.otp}"
    
from django.db import models
from django.contrib.auth.models import User
from hotels.models import Hotel  # assuming Hotel model is in hotels app


class ManagerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='manager_profile')
    hotel = models.OneToOneField(Hotel, on_delete=models.CASCADE, related_name='manager_profile')
    
    address = models.CharField(max_length=255, blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    available = models.BooleanField(default=True)
    password_plain = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"Manager Profile for {self.hotel.name}"



