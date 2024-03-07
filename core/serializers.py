from rest_framework import serializers
from .models import CustomUser, Client, Transporter, Order, Product

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
        cep = validated_data['cep']
        street = validated_data['street']
        number = validated_data['number']
        district = validated_data['district']
        city = validated_data['city']
        uf = validated_data['uf']

        # criação do cliente
        client = Client(
            user=user,
            name=name,
            birthday=birthday,
            cep=cep,
            street=street,
            number=number,
            district=district,
            city=city,
            uf=uf
        )

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
