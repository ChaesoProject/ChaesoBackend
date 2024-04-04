from djoser.views import UserViewSet as DjoserUserViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters import rest_framework as filters
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status
from rest_framework.authtoken.models import Token
from random import choice
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
    

# gerencia transporters
class TransporterViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.TransporterSerializer
    queryset = models.Transporter.objects.all()
    filter_backends = (filters.DjangoFilterBackend, )
    filterset_fields = ('user',)
    search_fields = ('user__username', 'user__email')

    # chamada quando um novo transporter é criado
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

    # atualiza dados do transporter e do usuário associado
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
    

class ProductViewSet(viewsets.ModelViewSet):
    queryset = models.Product.objects.all()
    serializer_class = serializers.ProductSerializer

    def create(self, request, *args, **kwargs):
        # verifica se já existe um produto com o mesmo nome
        existing_product = models.Product.objects.filter(name=request.data.get('name')).exists()
        if existing_product:
            return Response({'error': 'Product with this name already exists.'}, status=status.HTTP_400_BAD_REQUEST)

        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
class OrderViewSet(viewsets.ModelViewSet):
    queryset = models.Order.objects.all()
    serializer_class = serializers.OrderSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        # obtém o cliente associado ao usuário autenticado
        client = self.request.user.client

        # obtém o transportador, fazendo um sorteio se não for fornecido na requisição
        transporter_id = self.request.data.get('transporter')
        if transporter_id:
            transporter = get_object_or_404(models.Transporter, id=transporter_id)
        else:
            # se não houver ID de transportador fornecido, é feito o sorteio de um
            transporters = models.Transporter.objects.all()
            transporter = choice(transporters)

        serializer.save(client=client, transporter=transporter, status="Seu pedido saiu para entrega e está a caminho do seu endereço")

    def get_queryset(self):
        # verifica se o usuário autenticado é um cliente
        if hasattr(self.request.user, 'client'):
            # se for cliente, retorna os pedidos associados a ele
            try:
                client = self.request.user.client
                return self.queryset.filter(client=client)
            except models.CustomUser.client.RelatedObjectDoesNotExist:
                return self.queryset.none()
        # verifica se o usuário autenticado é um transportador
        elif hasattr(self.request.user, 'transporter'):
            # se for transportador, retorna os pedidos atribuídos a ele
            try:
                transporter = self.request.user.transporter
                return self.queryset.filter(transporter=transporter)
            except models.CustomUser.transporter.RelatedObjectDoesNotExist:
                return self.queryset.none()
        else:
            # se o usuário autenticado não for nem cliente nem transportador, retorna uma lista vazia
            print("Não é cliente nem transportador")
            return self.queryset.none()



