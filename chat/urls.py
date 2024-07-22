from django.urls import path
from rest_framework import routers

from .views import ChatRoomViewSet, ChatViewSet, MessageViewSet

router = routers.DefaultRouter()
router.register('chats', ChatViewSet)
router.register('chatrooms', ChatRoomViewSet)
router.register('messages', MessageViewSet)


urlpatterns = router.urls