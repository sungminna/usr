from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from chat.models import ChatRoom, Chat, Message
from django.urls import reverse


# Create your tests here.

class ChatRoomViewSetTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', email='<EMAIL>', password='<PASSWORD>')
        self.client = APIClient()

    def test_create_chatroom(self):
        url = reverse('chatroom-list')

        self.client.force_authenticate(user=self.user)
        initial_count = ChatRoom.objects.count()
        response = self.client.post(url, {'room_name': 'Test Chat Roomname'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(ChatRoom.objects.count(), initial_count + 1)
        self.assertEqual(ChatRoom.objects.first().room_name, 'Test Chat Roomname')
        self.assertEqual(ChatRoom.objects.latest('id').owner, self.user)

    def test_unauthenticated_create_chatroom(self):
        url = reverse('chatroom-list')
        initial_count = ChatRoom.objects.count()
        response = self.client.post(url, {'room_name': 'Test Chat Roomname'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(ChatRoom.objects.count(), initial_count)

    def test_get_chatroom_list(self):
        url = reverse('chatroom-list')
        self.client.force_authenticate(user=self.user)
        chatroom = ChatRoom.objects.create(room_name='Test Chat Roomname', owner=self.user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_chatroom_detail(self):
        url = reverse('chatroom-detail', kwargs={'pk': 1})
        self.client.force_authenticate(user=self.user)
        chatroom = ChatRoom.objects.create(room_name='Test Chat Roomname', owner=self.user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['room_name'], 'Test Chat Roomname')
        self.assertEqual(response.data['owner'], self.user.id)
        self.assertEqual(response.data['id'], chatroom.id)

    def test_update_chatroom(self):
        url = reverse('chatroom-detail', kwargs={'pk': 1})
        self.client.force_authenticate(user=self.user)
        chatroom = ChatRoom.objects.create(room_name='Test Chat Roomname', owner=self.user)
        response = self.client.put(url, {'room_name': 'Updated Test Chat Roomname'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['room_name'], 'Updated Test Chat Roomname')
        self.assertEqual(response.data['owner'], self.user.id)
        self.assertEqual(response.data['id'], chatroom.id)

    def test_delete_chatroom(self):
        url = reverse('chatroom-detail', kwargs={'pk': 1})
        self.client.force_authenticate(user=self.user)
        chatroom = ChatRoom.objects.create(room_name='Test Chat Roomname', owner=self.user)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(ChatRoom.objects.count(), 0)


class ChatViewSetTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', email='<EMAIL>', password='<PASSWORD>')
        self.chatroom = ChatRoom.objects.create(room_name='Test Chat Roomname', owner=self.user)
        self.client = APIClient()

    def test_create_chat(self):
        url = reverse('chat-list')
        self.client.force_authenticate(user=self.user)
        response = self.client.post(url, {'chatroom': self.chatroom.id}, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Chat.objects.count(), 1)
        self.assertEqual(response.data['chatroom'], self.chatroom.id)
        self.assertEqual(response.data['participant'], self.user.id)

    def test_unauthenticated_create_chat(self):
        url = reverse('chat-list')
        initial_count = Chat.objects.count()
        response = self.client.post(url, {'chatroom': self.chatroom.id}, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Chat.objects.count(), initial_count)

    def test_get_chat_list(self):
        url = reverse('chat-list')
        self.client.force_authenticate(user=self.user)
        chat = Chat.objects.create(chatroom=self.chatroom, participant=self.user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_chat_detail(self):
        url = reverse('chat-detail', kwargs={'pk': 1})
        self.client.force_authenticate(user=self.user)
        chat = Chat.objects.create(chatroom=self.chatroom, participant=self.user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['chatroom'], self.chatroom.id)
        self.assertEqual(response.data['participant'], self.user.id)
        self.assertEqual(response.data['id'], chat.id)

    def test_update_chat(self):
        pass

    def test_delete_chat(self):
        url = reverse('chat-detail', kwargs={'pk': 1})
        self.client.force_authenticate(user=self.user)
        chat = Chat.objects.create(chatroom=self.chatroom, participant=self.user)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Chat.objects.count(), 0)

class MessageViewSetTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', email='<EMAIL>', password='<PASSWORD>')
        self.chatroom = ChatRoom.objects.create(room_name='Test Chat Roomname', owner=self.user)
        self.chat = Chat.objects.create(chatroom=self.chatroom, participant=self.user)
        self.client = APIClient()

    def test_create_message(self):
        url = reverse('message-list')
        self.client.force_authenticate(user=self.user)
        response = self.client.post(url, {'chat_id': self.chat.id, 'text': 'Test Message Text'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Message.objects.count(), 1)
        self.assertEqual(response.data['chat'], self.chat.id)
        self.assertEqual(response.data['text'], 'Test Message Text')
        self.assertEqual(response.data['sender'], self.user.id)

    def test_unauthenticated_create_message(self):
        url = reverse('message-list')
        response = self.client.post(url, {'chat_id': self.chat.id, 'text': 'Test Message Text'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Message.objects.count(), 0)

    def test_get_message_list(self):
        url = reverse('message-list')
        self.client.force_authenticate(user=self.user)
        other_chat = Chat.objects.create(chatroom=self.chatroom, participant=self.user)
        message = Message.objects.create(chat=self.chat, text='Test Message Text', sender=self.user)
        response = self.client.get(url, {'chat_id': self.chat.id})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_message_detail(self):
        url = reverse('message-detail', kwargs={'pk': 1})
        self.client.force_authenticate(user=self.user)
        message = Message.objects.create(chat=self.chat, text='Test Message Text', sender=self.user)
        response = self.client.get(url, {'chat_id': self.chat.id})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['chat'], self.chat.id)
        self.assertEqual(response.data['text'], 'Test Message Text')
        self.assertEqual(response.data['sender'], self.user.id)
        self.assertEqual(response.data['id'], message.id)

    def test_update_message(self):
        url = reverse('message-detail', kwargs={'pk': 1})
        self.client.force_authenticate(user=self.user)
        message = Message.objects.create(chat=self.chat, text='Test Message Text', sender=self.user)
        response = self.client.put(url, {'text': 'Updated Test Message Text'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Message.objects.count(), 1)
        self.assertEqual(response.data['chat'], self.chat.id)
        self.assertEqual(response.data['text'], 'Updated Test Message Text')
        self.assertEqual(response.data['sender'], self.user.id)
        self.assertEqual(response.data['id'], message.id)

    def test_delete_message(self):
        url = reverse('message-detail', kwargs={'pk': 1})
        self.client.force_authenticate(user=self.user)
        message = Message.objects.create(chat=self.chat, text='Test Message Text', sender=self.user)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Message.objects.count(), 0)

