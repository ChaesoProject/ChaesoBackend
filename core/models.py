from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.contrib.auth import get_user_model
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
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE, blank=True, null=True)
    name = models.CharField(max_length=40)
    birthday = models.DateField()
    cep = models.CharField(max_length=10)
    street = models.CharField(max_length=100)
    number = models.IntegerField()
    district = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    uf = models.CharField(max_length=2)

    class Meta:
        verbose_name = 'Client'
        verbose_name_plural = 'Clients'

    def __str__(self):
        return f'{self.name}'
    

class Transporter(models.Model):
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE, blank=True, null=True)
    name = models.CharField(max_length=40)
    birthday = models.DateField()
    cnh = models.CharField(max_length=20)
    category_cnh = models.CharField(max_length=5)

    class Meta:
        verbose_name = 'Transporter'
        verbose_name_plural = 'Transporters'

    def __str__(self):
        return f'{self.client}, {self.cnh}'


class Order(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='orders', blank=True)
    transporter = models.ForeignKey(Transporter, on_delete=models.CASCADE, blank=True)
    products = models.ManyToManyField('Product')
    delivery_date = models.DateTimeField(null=True, blank=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    status = models.CharField(max_length=50, null=True, blank=True)

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
