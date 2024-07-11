from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import FirebaseTokenView


urlpatterns = [
    path('firebase-token/', FirebaseTokenView.as_view(), name='firebase-token-list'),
]