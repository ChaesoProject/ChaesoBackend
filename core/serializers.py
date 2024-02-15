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
    addresses = AddressSerializer(many=True, read_only=True)

    class Meta:
        model = Client
        fields = '__all__'

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
