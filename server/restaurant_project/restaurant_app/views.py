from django.shortcuts import render
from rest_framework.response import Response
from .serializers import UserRegistrationSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import login
from .serializers import UserAuthenticationSerializer
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics







class UserRegistrationView(generics.CreateAPIView):
    serializer_class = UserRegistrationSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({"detail": "User registered successfully."}, status=201)


class UserAuthenticationView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = UserAuthenticationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data
        login(request, user)

        
        token, created = Token.objects.get_or_create(user=user)

        return Response({"detail": "User logged in successfully.", "token": token.key})
