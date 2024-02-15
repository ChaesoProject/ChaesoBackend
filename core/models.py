from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.db import models


class CustomUserManager(BaseUserManager):
    def create_user(self, cpf, password=None, **extra_fields):
        if not cpf:
            raise ValueError("CPF is required to create a user.")

        user = self.model(cpf=cpf, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, cpf, password=None, **extra_fields):
        user = self.create_user(cpf, password, **extra_fields)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class CustomUser(AbstractBaseUser, PermissionsMixin):
    cpf = models.CharField(max_length=15, unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'cpf'

    def __str__(self):
        return self.cpf


class Client(models.Model):
    CLIENT = 'client'
    TRANSPORTER = 'transporter'
    TYPE_CHOICES = [
        (CLIENT, 'Client'),
        (TRANSPORTER, 'Transporter'),
    ]

    name = models.CharField(max_length=40)
    birthday = models.DateField()
    type = models.CharField(max_length=40, choices=TYPE_CHOICES)

    class Meta:
        verbose_name = 'Client'
        verbose_name_plural = 'Clients'

    def __str__(self):
        return f'{self.name}'


class Address(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='addresses')
    cep = models.CharField(max_length=10)
    street = models.CharField(max_length=100)
    number = models.IntegerField()
    district = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    uf = models.CharField(max_length=2)

    class Meta:
        verbose_name = 'Address'
        verbose_name_plural = 'Addresses'

    def __str__(self):
        return f'{self.client}, {self.street}'


class Transporter(models.Model):
    client = models.OneToOneField(Client, on_delete=models.CASCADE, related_name='transporter')
    cnh = models.CharField(max_length=20)
    category_cnh = models.CharField(max_length=5)

    class Meta:
        verbose_name = 'Transporter'
        verbose_name_plural = 'Transporters'

    def __str__(self):
        return f'{self.client}, {self.cnh}'


class Order(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='orders')
    transporter = models.ForeignKey(Transporter, on_delete=models.CASCADE)
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    date_order = models.DateField()
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=50)

    class Meta:
        verbose_name = 'Order'
        verbose_name_plural = 'Orders'

    def __str__(self):
        return f'{self.client}, {self.transporter}, {self.total_amount}'


class Product(models.Model):
    name = models.CharField(max_length=100)
    value = models.DecimalField(max_digits=10, decimal_places=2)
    weight_kg = models.CharField(max_length=100)
    photo = models.ImageField(upload_to='client_photos/', null=True, blank=True)

    class Meta:
            verbose_name = 'Product'
            verbose_name_plural = 'Products'

    def __str__(self):
        return f'{self.name}, {self.value}'

# Corrigir conflito de acesso reverso para grupos e permissões de usuário
CustomUser._meta.get_field('groups').remote_field.related_name = 'user_groups'
CustomUser._meta.get_field('user_permissions').remote_field.related_name = 'user_permissions_custom'
