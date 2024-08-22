from django.shortcuts import render
from authentication.models import CustomUser
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.views import APIView
from authentication.serializers import CustomUserSerializer,MyTokenObtainPairSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

# Create your views here.

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

class UserRegisterView(APIView):
    def post(self,request):
        serializer = CustomUserSerializer(data = request.data)
        serializer.is_valid(raise_exception = True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)