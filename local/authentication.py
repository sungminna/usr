from django.contrib.auth import get_user_model
from firebase_admin import auth
from rest_framework import exceptions, authentication
from .models import FirebaseToken

User = get_user_model()


class FirebaseAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        try:
            auth_header = request.META.get('HTTP_AUTHORIZATION')
            if not auth_header:
                return None
            token = auth_header.split(' ').pop()
            if token == 'undefined':
                # server component returns 'undefined' string as token
                # subject to change by frontend code
                return None
            decoded_token = auth.verify_id_token(token)
            firebase_uid = decoded_token['uid']
            token = FirebaseToken.objects.select_related('user').get(firebase_uid=firebase_uid)
            user = token.user
            return user, token
        except auth.InvalidIdTokenError:
            raise exceptions.AuthenticationFailed('Invalid Firebase ID Token')
