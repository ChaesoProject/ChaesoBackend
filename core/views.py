from djoser.views import UserViewSet as DjoserUserViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import viewsets, status, generics, permissions
from core import serializers


# realiza o registro personalizado de usuários
class CustomUserViewSet(DjoserUserViewSet):
    @action(detail=False, methods=['post'])
    def register(self, request):
        serializer = serializers.CustomUserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    