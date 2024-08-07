from django.db import IntegrityError
from rest_framework.exceptions import ValidationError

from django.shortcuts import render
from rest_framework import viewsets, status

from chat.models import ChatRoom, Chat, Message
from chat.serializers import ChatRoomSerializer, ChatSerializer, MessageSerializer
from local.authentication import FirebaseAuthentication
from local.permissions import IsParticipant, IsSenderOrReadOnly, IsParticipantOrReadOnly, IsOwnerOrReadOnly
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated

from rest_framework.response import Response
from rest_framework.decorators import action

from rest_framework.pagination import PageNumberPagination


# Create your views here.


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 5
    page_size_query_param = 'page_size'
    max_page_size = 100

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

    @action(detail=False, methods=['GET'])
    def check(self, request, *args, **kwargs):
        # /chat/messages/room_messages?room_id=<chatroom_id>
        room_id = request.query_params.get('room_id')
        if not room_id:
            return Response({'error': 'room_id is required'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            room = ChatRoom.objects.get(id=room_id)
            chat = self.queryset.filter(chatroom=room, participant=request.user).first()
            if chat:
                serializer = ChatSerializer(chat)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response({'participant': None}, status=status.HTTP_200_OK)
        except:
            return Response({'error': 'error'}, status=status.HTTP_400_BAD_REQUEST)

    def perform_create(self, serializer):
        chatroom = ChatRoom.objects.get(id=self.request.data['room_id'])
        try:
            serializer.save(participant=self.request.user, chatroom=chatroom)
        except IntegrityError:
            raise ValidationError({'error': 'already joined'})

class MessageViewSet(viewsets.ModelViewSet):
    authentication_classes = [FirebaseAuthentication]
    permission_classes = [IsAuthenticated, IsSenderOrReadOnly]
    queryset = Message.objects.all()
    pagination_class = StandardResultsSetPagination
    serializer_class = MessageSerializer


    @action(detail=False, methods=['GET'])
    def room_messages(self, request, *args, **kwargs):
        # /chat/messages/room_messages?room_id=<chatroom_id>
        room_id = request.query_params.get('room_id')
        if not room_id:
            return Response({'error': 'room_id is required'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            room = ChatRoom.objects.get(id=room_id)
            if not room:
                return Response({'error': 'room does not exist'}, status=status.HTTP_404_NOT_FOUND)
            chat = Chat.objects.filter(chatroom=room, participant=request.user).first()
            if not chat:
                return Response({'error': 'You are not a participant in this chat room'}, status=status.HTTP_403_FORBIDDEN)
            messages = self.queryset.filter(chat=chat).order_by('-timestamp')

            page = self.paginate_queryset(messages)
            if page is not None:
                serializer = MessageSerializer(page, many=True)
                return self.get_paginated_response(serializer.data)

            serializer = MessageSerializer(messages, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except:
            return Response({'error': 'error'}, status=status.HTTP_400_BAD_REQUEST)


    def perform_create(self, serializer):
        try:
            chat_id = self.request.data.get('chat_id')
            chat = Chat.objects.get(id=chat_id)
            if chat.participant == self.request.user or chat.chatroom.owner == self.request.user:
                serializer.save(chat=chat, sender=self.request.user)
        except Chat.DoesNotExist:
            return Response({'error': 'failed to create message'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
