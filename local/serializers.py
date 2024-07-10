from rest_framework import serializers
from .models import FirebaseToken

class FirebaseTokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = FirebaseToken
        fields = ('firebase_uid', 'token')

    def create(self, validated_data):
        user = self.context['request'].user
        firebase_token, created = FirebaseToken.objects.get_or_create(
            user=user,
            defaults={'firebase_uid': validated_data['firebase_uid'],
                      'token': validated_data['token']
                      }
        )
        return firebase_token
