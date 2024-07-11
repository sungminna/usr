from rest_framework import serializers
from .models import FirebaseToken

class FirebaseTokenCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = FirebaseToken
        fields = ('user', 'firebase_uid', 'token')

    def create(self, validated_data):
        user = self.context['request'].user
        firebase_uid = validated_data['firebase_uid']
        firebase_token = FirebaseToken.objects.create(user=user, firebase_uid=firebase_uid, **validated_data)
        return firebase_token
class FirebaseTokenUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = FirebaseToken
        fields = ('token', 'is_active')

    def put(self, validated_data):
        user = self.context['request'].user
        firebase_uid = validated_data['firebase_uid']
        firebase_token = FirebaseToken.objects.update(user=user, firebase_uid=firebase_uid, **validated_data)
        firebase_token.save()
        return firebase_token

class FirebaseTokenDeleteSerializer(serializers.ModelSerializer):
    class Meta:
        model = FirebaseToken
        fields = ('token', 'is_active', 'firebase_uid')

    def delete(self, validated_data):
        fb_token = validated_data['token']
        try:
            token = FirebaseToken.objects.get(token=fb_token)
            token.delete()
        except FirebaseToken.DoesNotExist:
            pass
        return None