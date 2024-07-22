from django.shortcuts import render
from rest_framework import viewsets

from chat.models import ChatRoom, Chat, Message
from chat.serializers import ChatRoomSerializer, ChatSerializer, MessageSerializer
from local.authentication import FirebaseAuthentication
from local.permissions import IsParticipant, IsSenderOrReadOnly, IsParticipantOrReadOnly, IsOwnerOrReadOnly
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated


# Create your views here.

class ChatRoomViewSet(viewsets.ModelViewSet):
    authentication_classes = [FirebaseAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    queryset = ChatRoom.objects.all()
    serializer_class = ChatRoomSerializer

class ChatViewSet(viewsets.ModelViewSet):
    authentication_classes = [FirebaseAuthentication]
    permission_classes = [IsAuthenticated, IsParticipantOrReadOnly]
    queryset = Chat.objects.all()
    serializer_class = ChatSerializer

class MessageViewSet(viewsets.ModelViewSet):
    authentication_classes = [FirebaseAuthentication]
    permission_classes = [IsAuthenticated, IsParticipant, IsSenderOrReadOnly]
    queryset = Message.objects.all()
    serializer_class = MessageSerializer

