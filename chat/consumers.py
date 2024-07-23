from channels.generic.websocket import AsyncJsonWebsocketConsumer
from channels.db import database_sync_to_async
from chat.models import ChatRoom, Chat, Message
from chat.serializers import MessageSerializer


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
            self.user = self.scope.get('user')

            if not await self.check_room_exists(self.room_id):
                raise ValueError(f'Room {self.room_id} does not exist')

            if not await self.check_chat_participants(user_id=self.user.id, room_id=self.room_id):
                raise ValueError(f'User {self.user.id} is not a chat participant in room {self.room_id}')

            self.group_name = self.get_group_name(self.room_id)
            await self.channel_layer.group_add(self.group_name, self.channel_name)
            await self.accept()
        except Exception as e:
            await self.send_json({'error': str(e)})
            await self.close()

    async def disconnect(self, close_code):
        try:
            if hasattr(self, 'group_name'):
                await self.channel_layer.group_discard(self.group_name, self.channel_name)
        except Exception as e:
            pass

    async def receive_json(self, content, **kwargs):
        try:
            message_type = content.get('type')
            if message_type == 'chat_message':
                text = content['text']
                room_id = content['room_id']
                if text:
                    chat = await self.get_chat(user_id=self.user.id, room_id=room_id)
                    saved_message = await self.save_message(text=text, chat=chat)
                    if saved_message:
                        await self.channel_layer.group_send(self.group_name, {
                            'type': 'chat_message',
                            'text': saved_message['text'],
                            'user_id': self.user.id,
                            'username': self.user.username,
                            'timestamp': saved_message['timestamp'],
                        })
        except KeyError as e:
            await self.send_json({'error': f'Missing required field: {str(e)}'})
        except Exception as e:
            await self.send_json({'error': str(e)})

    async def chat_message(self, event):
        try:
            text = event['text']
            user_id = event['user_id']
            username = event['username']
            timestamp = event['timestamp']
            await self.send_json({'text': text, 'user_id': user_id, 'username': username, 'timestamp': timestamp})
        except Exception as e:
            await self.send_json({'error': str(e)})

    @staticmethod
    def get_group_name(room_id):
        return f'chat_room_{room_id}'

    @database_sync_to_async
    def get_chat(self, user_id, room_id):
        chat = Chat.objects.filter(user_id=user_id, room_id=room_id).first()
        return chat


    @database_sync_to_async
    def save_message(self, text, chat):
        if not chat:
            raise ValueError(f'Chat {chat} does not exist')
        serializer = MessageSerializer(data={'text': text, 'chat': chat.id})
        if serializer.is_valid():
            saved_message = serializer.save()
            return {
                'id': saved_message.id,
                'text': saved_message.text,
                'timestamp': saved_message.timestamp.isoformat(),
            }
        return None

    @database_sync_to_async
    def check_room_exists(self, room_id):
        return ChatRoom.objects.filter(id=room_id).exists()

    @database_sync_to_async
    def check_chat_participants(self, user_id, room_id):
        return Chat.objects.filter(user=user_id, room=room_id).exists()