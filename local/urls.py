from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import FirebaseTokenView

router = DefaultRouter()
router.register('firebase-token', FirebaseTokenView.as_view(), basename='firebase-token')
urlpatterns = router.urls
