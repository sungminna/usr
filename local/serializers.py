from rest_framework import serializers
from .models import FirebaseToken
from django.contrib.auth.models import User


class FirebaseTokenSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    class Meta:
        model = FirebaseToken
        fields = ('id', 'user', 'firebase_uid', 'is_active')
