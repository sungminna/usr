from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.response import Response
from .models import Forum, Topic, Post, Comment, User
from django.contrib.auth.models import Group

from .serializers import ForumSerializer, TopicSerializer, PostSerializer, CommentSerializer, UserSerializer, \
    GroupSerializer

from django_filters.rest_framework import DjangoFilterBackend
from local.authentication import FirebaseAuthentication
from local.permissions import IsAuthorOrReadOnly

from rest_framework.pagination import PageNumberPagination


# Create your views here.

class StandardResultsSetPagination(PageNumberPagination):
    page_size = 5
    page_size_query_param = 'page_size'
    max_page_size = 100


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

    @action(detail=False, methods=['GET'])
    def groups(self, request, *args, **kwargs):
        user = request.user
        try:
            groups = user.groups.all()
            serializer = GroupSerializer(groups, many=True)
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(data={'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['PATCH'])
    def join_group(self, request, *args, **kwargs):
        user = request.user
        group_id = request.data['group_id']
        try:
            user.groups.add(group_id)
            return Response('User joined group', status=status.HTTP_200_OK)
        except:
            return Response('Can not join Group', status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['PATCH'])
    def leave_group(self, request, *args, **kwargs):
        user = request.user
        group_id = request.data['group_id']
        try:
            user.groups.remove(group_id)
            return Response('User left group', status=status.HTTP_200_OK)

        except:
            return Response('Can not leave Group', status=status.HTTP_400_BAD_REQUEST)


class GroupViewSet(viewsets.ModelViewSet):
    authentication_classes = []
    permission_classes = []
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


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
    permission_classes = [IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['topic_id']
    pagination_class = StandardResultsSetPagination

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):
    authentication_classes = [FirebaseAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]  # IsPostAuthorOrCommentAuthor
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['post_id']
    pagination_class = StandardResultsSetPagination

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
