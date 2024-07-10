from django.db import models
from django.contrib.auth.models import User, AbstractUser


# Create your models here.
class FirebaseToken(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    firebase_uid = models.CharField(max_length=255, unique=True)
    token = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
