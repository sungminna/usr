from django.contrib.auth import get_user_model
from firebase_admin import auth
from rest_framework import exceptions, authentication

User = get_user_model()

class FirebaseAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        try:
            auth_header = request.META('HTTP_AUTHORIZATION')
            if not auth_header:
                return None
            id_token = auth_header.split(' ').pop()
            decoded_token = auth.verify_id_token(id_token)
            uid = decoded_token['uid']
            user = User.objects.get(fb_token=uid)
            return user, None
        except auth.InvalidIdTokenError:
            raise exceptions.AuthenticationFailed('Invalid Firebase ID Token')
