from rest_framework import serializers

from chat.models import ChatRoom, Chat, Message


class ChatRoomSerializer(serializers.HyperlinkedModelSerializer):
    owner = serializers.PrimaryKeyRelatedField(read_only=True)
    owner_name = serializers.ReadOnlyField(source='owner.username')
    class Meta:
        model = ChatRoom
        fields = ('id', 'room_name', 'owner', 'owner_name', 'timestamp')
        read_only_fields = ('id', 'owner', 'owner_name', 'timestamp')

class ChatSerializer(serializers.HyperlinkedModelSerializer):
    chatroom = serializers.PrimaryKeyRelatedField(read_only=True)
    participant = serializers.PrimaryKeyRelatedField(read_only=True)
    class Meta:
        model = Chat
        fields = ('id', 'chatroom', 'participant', 'timestamp')
        read_only_fields = ('id', 'participant', 'chatroom', 'timestamp')

class MessageSerializer(serializers.HyperlinkedModelSerializer):
    chat = serializers.PrimaryKeyRelatedField(read_only=True)
    sender = serializers.PrimaryKeyRelatedField(read_only=True)
    class Meta:
        model = Message
        fields = ('id', 'chat', 'sender', 'text', 'timestamp')
        read_only_fields = ('id', 'chat', 'sender', 'timestamp')
