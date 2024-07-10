from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ForumViewSet, TopicViewSet, PostViewSet, CommentViewSet

router = DefaultRouter()
router.register('forums', ForumViewSet)
router.register('topics', TopicViewSet)
router.register('posts', PostViewSet)
router.register('comments', CommentViewSet)

urlpatterns = router.urls
