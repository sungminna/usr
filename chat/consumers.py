from channels.generic.websocket import AsyncJsonWebsocketConsumer
from channels.db import database_sync_to_async
from chat.models import ChatRoom, Chat, Message
from django.contrib.auth.models import User
class ChatConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        try:
            url_route = self.scope.get('url_route', None)
            if not url_route:
                self.room_id = self.scope['path'].split('/')[2]
            else:
                self.room_id = self.scope['url_route']['kwargs']['room_id']

            if not self.scope.get('user') or self.scope.get('user').is_anonymous:
                await self.close()
                return
            user_id = self.scope.get('user').id

            if not await self.check_room_exists(self.room_id):
                raise ValueError(f'Room {self.room_id} does not exist')

            if not await self.check_chat_participants(user_id=user_id, room_id=self.room_id):
                raise ValueError(f'User {user_id} is not a chat participant in room {self.room_id}')

            group_name = self.get_group_name(self.room_id)
            await self.channel_layer.group_add(group_name, self.channel_name)
            await self.accept()
        except Exception as e:
            await self.send_json({'error': str(e)})
            await self.close()


    async def disconnect(self, close_code):
        try:
            group_name = self.get_group_name(self.room_id)
            await self.channel_layer.group_discard(group_name, self.channel_name)
        except Exception as e:
            pass

    async def receive_json(self, content, **kwargs):
        try:
            text = content['text']
            user_id = self.scope['user'].id
            room_id = content['room_id']

            chat = await self.get_chat(user_id=user_id, room_id=room_id)
            group_name = self.get_group_name(room_id)
            await self.save_message(text=text, chat=chat)
            await self.channel_layer.group_send(group_name, {
                'type': 'chat_message',
                'text': text,
                'user_id': user_id,
            })
        except Exception as e:
            await self.send_json({'error': str(e)})

    async def chat_message(self, event):
        try:
            text = event['text']
            user_id = event['user_id']
            await self.send_json({'text': text, 'user_id': user_id})
        except Exception as e:
            await self.send_json({'error': str(e)})

    @staticmethod
    def get_group_name(room_id):
        return f'chat_room_{room_id}'

    @database_sync_to_async
    def create_chatroom(self, room_name):
        chatroom = ChatRoom.objects.create(room_name=room_name)
        return chatroom

    @database_sync_to_async
    def get_chatroom(self, room_id):
        chatroom = ChatRoom.objects.get(id=room_id)
        return chatroom

    @database_sync_to_async
    def get_or_create_chatroom(self, room_name):
        chatroom = ChatRoom.objects.get_or_create(room_name=room_name)
        return chatroom

    @database_sync_to_async
    def get_chat(self, user_id, room_id):
        user = User.objects.get(id=user_id)
        chatroom = ChatRoom.objects.filter(id=room_id).first()
        chat = Chat.objects.filter(user=user, room=chatroom).first()
        return chat

    @database_sync_to_async
    def get_or_create_chat(self, user_id, room_id):
        user = User.objects.get(id=user_id)
        chat, created = Chat.objects.get_or_create(user=user, room=room_id)
        return chat

    @database_sync_to_async
    def save_message(self, text, chat):
        if not chat:
            raise ValueError(f'Chat {chat} does not exist')
        Message.objects.create(text=text, chat=chat)

    @database_sync_to_async
    def check_room_exists(self, room_id):
        return ChatRoom.objects.filter(id=room_id).exists()

    @database_sync_to_async
    def check_chat_participants(self, user_id, room_id):
        return Chat.objects.filter(user=user_id, room=room_id).exists()