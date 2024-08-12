from rest_framework.routers import DefaultRouter
from .views import ForumViewSet, TopicViewSet, PostViewSet, CommentViewSet, UserViewSet, GroupViewSet

router = DefaultRouter()
router.register('users', UserViewSet)
router.register('groups', GroupViewSet)
router.register('forums', ForumViewSet)
router.register('topics', TopicViewSet)
router.register('posts', PostViewSet)
router.register('comments', CommentViewSet)

urlpatterns = router.urls
