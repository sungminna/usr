from channels.db import database_sync_to_async
from django.contrib.auth import get_user_model
from firebase_admin import auth
from local.models import FirebaseToken

User = get_user_model()

@database_sync_to_async
def get_user(token):
    try:
        if token == 'undefined':
            # server component returns 'undefined' string as token
            # subject to change by frontend code
            return None
        decoded_token = auth.verify_id_token(token)
        firebase_uid = decoded_token['uid']
        token = FirebaseToken.objects.select_related('user').get(firebase_uid=firebase_uid)
        user = token.user
        return user
    except Exception as e:
        return None

class TokenAuthMiddleware:
    def __init__(self, inner):
        self.inner = inner

    async def __call__(self, scope, receive, send):
        header = dict(scope['headers'])
        if b'authorization' in header:
            token = header['authorization'].decode().split()[1]
            scope['user'] = await get_user(token)
        return await self.inner(scope, receive, send)

