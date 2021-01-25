from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from .serializer import UserSerializer
from .models import MTUser
from rest_framework.response import Response
from django.contrib.auth.hashers import make_password


class UserRegisterView(ModelViewSet):
    http_method_names = ['post', 'patch']
    authentication_classes = ()
    permission_classes = ()
    queryset = MTUser.objects.all()
    serializer_class = UserSerializer

