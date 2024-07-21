from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.response import Response
from .models import Forum, Topic, Post, Comment, User
from .serializers import ForumSerializer, TopicSerializer, PostSerializer, CommentSerializer, UserSerializer

from django_filters.rest_framework import DjangoFilterBackend
from local.authentication import FirebaseAuthentication
from local.permissions import isAuthorOrReadOnly, IsFirebaseAuthenticated

# Create your views here.

class UserViewSet(viewsets.ViewSet):
    authentication_classes = [FirebaseAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = User.objects.all()
    serializer_class = UserSerializer

    @action(detail=False, methods=['GET'])
    def me(self, request, *args, **kwargs):
        # /community/users/me
        user = request.user
        data = {'id': user.id,
                'username': user.username,
                }
        return Response(data, status=status.HTTP_200_OK)

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
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['forum_id']

class PostViewSet(viewsets.ModelViewSet):
    authentication_classes = [FirebaseAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly, isAuthorOrReadOnly]
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['topic_id']

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

class CommentViewSet(viewsets.ModelViewSet):
    authentication_classes = [FirebaseAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly, isAuthorOrReadOnly]
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['post_id']
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
