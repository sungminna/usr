from rest_framework import status
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.response import Response
from rest_framework.views import APIView
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

    def _verify_token(self, token):
        if not token:
            return Response({'message': 'Token is missing'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            return auth.verify_id_token(token)
        except auth.InvalidIdTokenError:
            return Response({'message': 'Token is invalid'}, status=status.HTTP_401_UNAUTHORIZED)

    def _get_or_create_user(self, username, email):

        is_user_exists = User.objects.filter(email=email).exists()
        if not is_user_exists:
            user, created = User.objects.get_or_create(username=username, email=email)
            if created:
                user.set_unusable_password()
                user.save()
                return user
        else:
            return None
    def _create_or_update_token(self, user, firebase_uid, request=None):
        data = {
            'user': user.pk,
            'firebase_uid': firebase_uid,
            'is_active': True,
        }
        context = {'request': request} if request else {}
        token = FirebaseToken.objects.filter(firebase_uid=firebase_uid).first()
        if token:
            serializer = FirebaseTokenSerializer(token, data=data, partial=True, context=context)
        else:
            serializer = FirebaseTokenSerializer(data=data, partial=True, context=context)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request):
        try:
            token = request.data.get('token')
            decoded_token = self._verify_token(token)
            if isinstance(decoded_token, Response):
                return decoded_token
            firebase_uid = decoded_token.get('uid')
            email = decoded_token.get('email')
            username = request.data.get('username')
            user = self._get_or_create_user(username, email)
            if user != None:
                return self._create_or_update_token(user, firebase_uid, request)
            else:
                return Response({'message': 'Email already exists'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        try:
            if not request.user.is_authenticated:
                return Response({'message': 'Authentication required'}, status=status.HTTP_401_UNAUTHORIZED)
            token = request.data.get('token')
            decoded_token = self._verify_token(token)
            if isinstance(decoded_token, Response):
                return decoded_token
            firebase_uid = decoded_token.get('uid')
            try:
                fb_token = FirebaseToken.objects.get(firebase_uid=firebase_uid)
                if fb_token.user != request.user:
                    return Response({'message': 'User does not match'}, status=status.HTTP_403_FORBIDDEN)
            except FirebaseToken.DoesNotExist:
                return Response({'message': 'Token not found'}, status=status.HTTP_404_NOT_FOUND)
            fb_token.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except AuthenticationFailed:
            return Response({'message': 'Authentication failed'}, status=status.HTTP_401_UNAUTHORIZED)
        except Exception as e:
            return Response({'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)
