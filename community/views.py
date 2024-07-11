from django.shortcuts import render
from rest_framework import viewsets

from .models import Forum, Topic, Post, Comment
from .serializers import ForumSerializer, TopicSerializer, PostSerializer, CommentSerializer

# Create your views here.

class ForumViewSet(viewsets.ModelViewSet):
    authentication_classes = []
    permission_classes = []
    queryset = Forum.objects.all()
    serializer_class = ForumSerializer

class TopicViewSet(viewsets.ModelViewSet):
    authentication_classes = []
    permission_classes = []
    queryset = Topic.objects.all()
    serializer_class = TopicSerializer

class PostViewSet(viewsets.ModelViewSet):
    authentication_classes = []
    permission_classes = []
    queryset = Post.objects.all()
    serializer_class = PostSerializer

class CommentViewSet(viewsets.ModelViewSet):
    authentication_classes = []
    permission_classes = []
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer



