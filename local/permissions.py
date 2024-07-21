import base64

from rest_framework.exceptions import AuthenticationFailed
from rest_framework.permissions import BasePermission, SAFE_METHODS
from firebase_admin import auth
class isAuthorOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return obj.author == request.user

class IsFirebaseAuthenticated(BasePermission):
    def has_permission(self, request, view):
        auth_header = request.META.get('HTTP_AUTHORIZATION')
        if not auth_header:
            return False

        try:
            token = auth_header.split(" ")[1]
            decoded_token = auth.verify_id_token(token)
            return True

        except auth.InvalidIdTokenError:
            raise AuthenticationFailed('Invalid authorization token')
        except IndexError:
            return False
        except Exception as e:
            print(e)
            return False