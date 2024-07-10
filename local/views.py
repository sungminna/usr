from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

from rest_framework import viewsets
from .models import FirebaseToken
from .serializers import FirebaseTokenSerializer
from firebase_admin import auth

# Create your views here.

class FirebaseTokenView(APIView):
    permission_classes = [IsAuthenticated,]

    def post(self, request):
        token = request.data.get('token')
        if not token:
            return Response({'message': 'Token is missing'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            decoded_token = auth.verify_id_token(token)
            firebase_uid = decoded_token['uid']

            data = {
                'firebase_uid': firebase_uid,
                'token': token,
            }
            serializer = FirebaseTokenSerializer(data=data, context={'request': request})
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class FirebaseTokenViewSet(viewsets.ModelViewSet):
    queryset = FirebaseToken.objects.all()
    serializer_class = FirebaseTokenSerializer

