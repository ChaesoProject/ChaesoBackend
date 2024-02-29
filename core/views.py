from djoser.views import UserViewSet as DjoserUserViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters import rest_framework as filters
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status, generics, permissions
from rest_framework.authtoken.models import Token
from core import serializers, models


# realiza o registro personalizado de usuários
class CustomUserViewSet(DjoserUserViewSet):
    @action(detail=False, methods=['post'])
    def register(self, request):
        serializer = serializers.CustomUserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


# gerencia clientes
class ClientViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.ClientSerializer
    queryset = models.Client.objects.all()
    filter_backends = (filters.DjangoFilterBackend, )
    filterset_fields = ('user',)
    search_fields = ('user__username', 'user__email')

    # chamada quando um novo cliente é criado
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)

        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()

        # deleta o usuário associado
        if instance.user:
            user_id = instance.user.id
            user = get_object_or_404(models.CustomUser, id=user_id)
            user.delete()

        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

    # atualiza dados do cliente e do usuário associado
    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        # atualizar dados do usuário
        user_data = request.data.get('user', {})
        if user_data:
            user_instance = instance.user
            user_serializer = serializers.CustomUserSerializer(user_instance, data=user_data, partial=True)
            user_serializer.is_valid(raise_exception=True)
            user_serializer.save()

            # desloga o usuário após a atualização da senha
            Token.objects.filter(user=user_instance).delete()

        return Response(serializer.data, status=status.HTTP_200_OK)  