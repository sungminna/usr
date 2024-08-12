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
    chat = serializers.PrimaryKeyRelatedField(queryset=Chat.objects.all())
    sender = serializers.PrimaryKeyRelatedField(read_only=True)
    sender_name = serializers.SerializerMethodField()

    class Meta:
        model = Message
        fields = ('id', 'chat', 'sender', 'sender_name', 'text', 'timestamp')
        read_only_fields = ('id', 'sender', 'sender_name', 'timestamp')

    def create(self, validated_data):
        validated_data['sender'] = self.context['request'].get('user')
        return super().create(validated_data)

    def get_sender_name(self, obj):
        return obj.sender.username if obj.sender else None

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['sender_name'] = self.get_sender_name(instance)
        return representation
