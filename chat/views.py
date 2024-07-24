from django.shortcuts import render
from rest_framework import viewsets, status

from chat.models import ChatRoom, Chat, Message
from chat.serializers import ChatRoomSerializer, ChatSerializer, MessageSerializer
from local.authentication import FirebaseAuthentication
from local.permissions import IsParticipant, IsSenderOrReadOnly, IsParticipantOrReadOnly, IsOwnerOrReadOnly
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated

from rest_framework.response import Response
from rest_framework.decorators import action

# Create your views here.

class ChatRoomViewSet(viewsets.ModelViewSet):
    authentication_classes = [FirebaseAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    queryset = ChatRoom.objects.all()
    serializer_class = ChatRoomSerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class ChatViewSet(viewsets.ModelViewSet):
    authentication_classes = [FirebaseAuthentication]
    permission_classes = [IsAuthenticated, IsParticipantOrReadOnly]
    queryset = Chat.objects.all()
    serializer_class = ChatSerializer

    def perform_create(self, serializer):
        chatroom = ChatRoom.objects.get(id=self.request.data['chatroom'])
        serializer.save(participant=self.request.user, chatroom=chatroom)

class MessageViewSet(viewsets.ModelViewSet):
    authentication_classes = [FirebaseAuthentication]
    permission_classes = [IsAuthenticated, IsParticipant, IsSenderOrReadOnly]
    queryset = Message.objects.all()
    serializer_class = MessageSerializer

    @action(detail=False, methods=['GET'])
    def room_messages(self, request, *args, **kwargs):
        # /chat/messages/room_messages?room_id=<chatroom_id>
        room_id = request.query_params.get('room_id')
        if not room_id:
            return Response({'error': 'room_id is required'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            room = ChatRoom.objects.get(id=room_id)
        except:
            return Response({'error': 'room does not exist'}, status=status.HTTP_404_NOT_FOUND)
        messages = self.queryset.filter(chatroom=room).order_by('-created_at')
        serializer = MessageSerializer(messages, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


    def perform_create(self, serializer):
        try:
            chat_id = self.request.data.get('chat_id')
            chat = Chat.objects.get(id=chat_id)
            if chat.participant == self.request.user or chat.chatroom.owner == self.request.user:
                serializer.save(chat=chat, sender=self.request.user)
        except Chat.DoesNotExist:
            return Response({'error': 'failed to create message'}, status=status.HTTP_400_BAD_REQUEST)
