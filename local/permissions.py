import base64

from rest_framework.exceptions import AuthenticationFailed
from rest_framework.permissions import BasePermission, SAFE_METHODS
from firebase_admin import auth
from chat.models import Chat


class IsAuthorOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return obj.author == request.user

class IsPostAuthorOrCommentAuthor(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return request.user == obj.post.author or request.user == obj.author


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

class IsParticipant(BasePermission):
    def has_permission(self, request, view):
        if request.method != 'GET':
            # if not GET return True to handle object perm
            return True
        chat_id = request.query_params.get('chat_id')
        if not chat_id:
            return False
        try:
            chat = Chat.objects.filter(id=chat_id).first()
        except Chat.DoesNotExist:
            return False
        return request.user == chat.participant


class IsOwnerOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return obj.owner == request.user

class IsParticipantOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return obj.participant == request.user

class IsSenderOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return obj.sender == request.user