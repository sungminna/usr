from django.urls import path
from .views import FirebaseTokenView


urlpatterns = [
    path('firebase-token/', FirebaseTokenView.as_view(), name='firebase-token-list'),
]
