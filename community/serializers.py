from django.contrib.auth.models import User, Group
from rest_framework import serializers
from .models import Forum, Topic, Post, Comment


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'groups')


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ('id', 'name')


class ForumSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Forum
        fields = ('id', 'title', 'description')


class TopicSerializer(serializers.HyperlinkedModelSerializer):
    forum = serializers.PrimaryKeyRelatedField(queryset=Forum.objects.all())

    class Meta:
        model = Topic
        fields = ('id', 'title', 'description', 'created_at', 'forum')


class PostSerializer(serializers.HyperlinkedModelSerializer):
    topic = serializers.PrimaryKeyRelatedField(queryset=Topic.objects.all())
    author = serializers.PrimaryKeyRelatedField(read_only=True)
    username = serializers.ReadOnlyField(source='author.username')

    class Meta:
        model = Post
        fields = ('id', 'content', 'created_at', 'author', 'topic', 'username')


class CommentSerializer(serializers.HyperlinkedModelSerializer):
    post = serializers.PrimaryKeyRelatedField(queryset=Post.objects.all())
    author = serializers.PrimaryKeyRelatedField(read_only=True)
    username = serializers.ReadOnlyField(source='author.username')

    class Meta:
        model = Comment
        fields = ('id', 'content', 'created_at', 'author', 'post', 'username')
