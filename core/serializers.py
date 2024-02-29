from rest_framework import serializers
from .models import CustomUser, Client, Address, Transporter, Order, Product

class CustomUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = CustomUser
        fields = ("cpf", "password")

    def create(self, validated_data):
        password = validated_data.pop("password", None)
        user = CustomUser.objects.create_user(**validated_data, password=password)
        return user

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        instance = super().update(instance, validated_data)

        if password:
            instance.set_password(password)
            instance.save()

        return instance

class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = '__all__'

class ClientSerializer(serializers.ModelSerializer):
    user = CustomUserSerializer(many=False, read_only=True)

    class Meta:
        model = Client
        fields = '__all__'

    def create(self, validated_data):
        user = self.context['request'].user

        # verifica se já existe um cliente para este usuário
        client = Client.objects.filter(user=user).first()
        if client:
            raise serializers.ValidationError("Cliente já existe para este usuário.")
        
        # campos obrigatórios
        name = validated_data['name']
        birthday = validated_data['birthday']
        type = validated_data['type']

        # criação do cliente
        client = Client(
            user=user,
            name=name,
            birthday=birthday,
            type=type
        )

        # Verifica se há dados para o endereço
        address_data = validated_data.get('address', None)
        if address_data:
            address_serializer = AddressSerializer(data=address_data)
            address_serializer.is_valid(raise_exception=True)
            address = address_serializer.save()
            client.address = address

        client.save()
        return client

    

class TransporterSerializer(serializers.ModelSerializer):
    client = ClientSerializer()

    class Meta:
        model = Transporter
        fields = '__all__'

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'
