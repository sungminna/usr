from django.test import TestCase
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Forum, Topic, Post, Comment

# Create your tests here.


class ForumAPITestCase(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.client = APIClient()
        cls.forum_data = {'title': 'Test Forum', 'description': 'Test Description'}

    def test_create_forum(self):
        url = reverse('forum-list')
        response = self.client.post(url, data=self.forum_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Forum.objects.count(), 1)
        self.assertEqual(response.data['title'], 'Test Forum')
        self.assertEqual(response.data['description'], 'Test Description')

    def test_get_forum_list(self):
        forum = Forum.objects.create(title='Test Forum', description='Test Description')
        url = reverse('forum-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_forum_detail(self):
        forum = Forum.objects.create(title='Test Forum', description='Test Description')
        url = reverse('forum-detail', kwargs={'pk': forum.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Test Forum')
        self.assertEqual(response.data['description'], 'Test Description')

    def test_update_forum(self):
        forum = Forum.objects.create(title='Test Forum', description='Test Description')
        updated_data = {'title': 'Test Updated Title', 'description': 'Test Updated Description'}
        url = reverse('forum-detail', kwargs={'pk': forum.pk})
        response = self.client.put(url, updated_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Test Updated Title')
        self.assertEqual(response.data['description'], 'Test Updated Description')

    def test_delete_forum(self):
        forum = Forum.objects.create(title='Test Forum', description='Test Description')
        url = reverse('forum-detail', kwargs={'pk': forum.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Forum.objects.count(), 0)

class TopicAPITestCase(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.client = APIClient()
        cls.forum_data = {'title': 'Test Forum', 'description': 'Test Description'}
        cls.forum = Forum.objects.create(title='Test Forum', description='Test Description')

    def test_create_topic(self):
        url = reverse('topic-list')
        data = {'title': 'Test Topic', 'description': 'Test Description', 'forum': self.forum.pk}
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Topic.objects.count(), 1)
        self.assertEqual(response.data['title'], 'Test Topic')
        self.assertEqual(response.data['description'], 'Test Description')
        self.assertEqual(response.data['forum'], self.forum.pk)

    def test_get_topic_list(self):
        topic = Topic.objects.create(title='Test Topic', description='Test Description', forum=self.forum)
        url = reverse('topic-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_topic_detail(self):
        topic = Topic.objects.create(title='Test Topic', description='Test Description', forum=self.forum)
        url = reverse('topic-detail', kwargs={'pk': topic.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Test Topic')
        self.assertEqual(response.data['description'], 'Test Description')
        self.assertEqual(response.data['forum'], self.forum.pk)

    def test_update_topic(self):
        topic = Topic.objects.create(title='Test Topic', description='Test Description', forum=self.forum)
        updated_data = {'title': 'Test Updated Title', 'description': 'Test Updated Description', 'forum': self.forum.pk}
        url = reverse('topic-detail', kwargs={'pk': topic.pk})
        response = self.client.put(url, updated_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Test Updated Title')
        self.assertEqual(response.data['description'], 'Test Updated Description')
        self.assertEqual(response.data['forum'], self.forum.pk)

    def test_delete_topic(self):
        topic = Topic.objects.create(title='Test Topic', description='Test Description', forum=self.forum)
        url = reverse('topic-detail', kwargs={'pk': topic.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Topic.objects.count(), 0)

class PostAPITestCase(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.client = APIClient()
        cls.user = User.objects.create_user(username='testuser', email='<EMAIL>', password='<PASSWORD>')
        cls.forum = Forum.objects.create(title='Test Forum', description='Test Description')
        cls.topic = Topic.objects.create(title='Test Topic', description='Test Description', forum=cls.forum)

    def test_create_post(self):
        url = reverse('post-list')
        data = {'content': 'Test Content', 'author': self.user.pk, 'topic': self.topic.pk}
        print(data)
        print(url)
        response = self.client.post(url, data=data)
        print(response)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Post.objects.count(), 1)
        self.assertEqual(response.data['content'], 'Test Content')
        self.assertEqual(response.data['author'], self.user.pk)
        self.assertEqual(response.data['topic'], self.topic.pk)

    def test_get_post_list(self):
        post = Post.objects.create(content='Test Content', author=self.user, topic=self.topic)
        url = reverse('post-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_post_detail(self):
        post = Post.objects.create(content='Test Content', author=self.user, topic=self.topic)
        url = reverse('post-detail', kwargs={'pk': post.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['content'], 'Test Content')
        self.assertEqual(response.data['author'], self.user.pk)
        self.assertEqual(response.data['topic'], self.topic.pk)

    def test_update_post(self):
        post = Post.objects.create(content='Test Content', author=self.user, topic=self.topic)
        updated_data = {'content': 'Test Updated Content', 'author': self.user.pk, 'topic': self.topic.pk}
        url = reverse('post-detail', kwargs={'pk': post.pk})
        response = self.client.put(url, updated_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['content'], 'Test Updated Content')
        self.assertEqual(response.data['topic'], self.topic.pk)
        self.assertEqual(response.data['author'], self.user.pk)

    def test_delete_post(self):
        post = Post.objects.create(content='Test Content', author=self.user, topic=self.topic)
        url = reverse('post-detail', kwargs={'pk': post.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Post.objects.count(), 0)

class CommentAPITestCase(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.client = APIClient()
        cls.user = User.objects.create_user(username='testuser', email='<EMAIL>', password='<PASSWORD>')
        cls.forum = Forum.objects.create(title='Test Forum', description='Test Description')
        cls.topic = Topic.objects.create(title='Test Topic', description='Test Description', forum=cls.forum)
        cls.post = Post.objects.create(content='Test Content', author=cls.user, topic=cls.topic)

    def test_create_comment(self):
        url = reverse('comment-list')
        data = {'content': 'Test Content', 'author': self.user.pk, 'post': self.post.pk}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Comment.objects.count(), 1)
        self.assertEqual(response.data['content'], 'Test Content')
        self.assertEqual(response.data['author'], self.user.pk)
        self.assertEqual(response.data['post'], self.post.pk)


    def test_get_comment_list(self):
        comment = Comment.objects.create(content='Test Content', author=self.user, post=self.post)
        url = reverse('comment-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


    def test_get_comment_detail(self):
        comment = Comment.objects.create(content='Test Content', author=self.user, post=self.post)
        url = reverse('comment-detail', kwargs={'pk': comment.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['content'], 'Test Content')
        self.assertEqual(response.data['author'], self.user.pk)
        self.assertEqual(response.data['post'], self.post.pk)

    def test_update_comment(self):
        comment = Comment.objects.create(content='Test Content', author=self.user, post=self.post)
        updated_data = {'content': 'Test Updated Content', 'author': self.user.pk, 'post': self.post.pk}
        url = reverse('comment-detail', kwargs={'pk': comment.pk})
        response = self.client.put(url, updated_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['content'], 'Test Updated Content')
        self.assertEqual(response.data['author'], self.user.pk)
        self.assertEqual(response.data['post'], self.post.pk)

    def test_delete_comment(self):
        comment = Comment.objects.create(content='Test Content', author=self.user, post=self.post)
        url = reverse('comment-detail', kwargs={'pk': comment.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Comment.objects.count(), 0)

