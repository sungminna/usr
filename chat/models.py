from django.db import models
from django.contrib.auth.models import User
from django.db.models import UniqueConstraint

# Create your models here.

class ChatRoom(models.Model):
    room_name = models.CharField(max_length=100)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-id']

class Chat(models.Model):
    chatroom = models.ForeignKey(ChatRoom, on_delete=models.CASCADE)
    participant = models.ForeignKey(User, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            UniqueConstraint(fields=['chatroom', 'participant'], name='unique_participant_chatroom')
        ]
        ordering = ['-id']

class Message(models.Model):
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE)
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-id']