from channels.db import database_sync_to_async
from django.contrib.auth import get_user_model
from channels.middleware import BaseMiddleware
from firebase_admin import auth
from local.models import FirebaseToken
from django.contrib.auth.models import AnonymousUser
from local.authentication import FirebaseAuthentication


class TokenAuthMiddleware(BaseMiddleware):
    def __init__(self, inner):
        super().__init__(inner)
        self.firebase_auth = FirebaseAuthentication()

    async def __call__(self, scope, receive, send):
        headers = dict(scope['headers'])
        auth_header = headers.get(b'authorization', b'').decode()
        if auth_header.startswith('Bearer '):
            token = auth_header.split(' ')[1]
            scope['user'] = await self.authenticate(token)
        else:
            scope['user'] = None
        return await super().__call__(scope, receive, send)

    @database_sync_to_async
    def authenticate(self, token):
        if not token:
            return None
        if token == 'undefined':
            return None
        try:
            decoded_token = auth.verify_id_token(token)
            firebase_uid = decoded_token['uid']
            firebase_token = FirebaseToken.objects.select_related('user').get(firebase_uid=firebase_uid)
            return firebase_token.user

        except auth.InvalidIdTokenError:
            return None
        except Exception as e:
            return None
