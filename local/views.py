from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework.permissions import AllowAny

from .models import FirebaseToken
from .serializers import FirebaseTokenSerializer
from firebase_admin import auth
from django.contrib.auth.models import User
from .authentication import FirebaseAuthentication
# Create your views here.

class FirebaseTokenView(APIView):
    permission_classes = [AllowAny, ]
    def get_authenticators(self):
        if self.request.method in ['PUT', 'DELETE']:
            return [FirebaseAuthentication()]
        return []


    def post(self, request):
        print(request.data)
        token = request.data.get('token')
        if not token:
            return Response({'message': 'Token is missing'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            decoded_token = auth.verify_id_token(token)
            firebase_uid = decoded_token.get('uid')
            email = decoded_token.get('email')
            username = request.data.get('username')
            user, created = User.objects.get_or_create(username=username, email=email)
            if created:
                user.set_unusable_password()
                user.save()
            data = {
                'user': user.pk,
                'firebase_uid': firebase_uid,
                'is_active': True,
            }
            serializer = FirebaseTokenSerializer(data=data)
            print(serializer)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except auth.InvalidIdTokenError:
            return Response({'message': 'Token is invalid'}, status=status.HTTP_401_UNAUTHORIZED)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request):
        token = request.data.get('token')
        if not token:
            return Response({'message': 'Token is missing'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            decoded_token = auth.verify_id_token(token)
            firebase_uid = decoded_token.get('uid')
            username = request.data.get('username')
            email = decoded_token.get('email')
            user, created = User.objects.get_or_create(username=username, email=email)

            data = {
                'user': user.pk,
                'firebase_uid': firebase_uid,
                'is_active': True,
            }
            serializer = FirebaseTokenSerializer(data=data, partial=True, context={'request': request})
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        except auth.InvalidIdTokenError:
            return Response({'message': 'Token is invalid'}, status=status.HTTP_401_UNAUTHORIZED)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        try:
            token = request.data.get('token')
            decoded_token = auth.verify_id_token(token)
            firebase_uid = decoded_token.get('uid')
            if not token:
                return Response({'message': 'Token is missing'}, status=status.HTTP_400_BAD_REQUEST)
            fb_token = FirebaseToken.objects.get(firebase_uid=firebase_uid)
            if fb_token:
                fb_token.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
        except FirebaseToken.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

