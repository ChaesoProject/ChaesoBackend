from django.contrib import admin
from .models import CustomUser, Client, Address, Transporter, Order, Product


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('cpf', 'is_active', 'is_staff')


@admin.register(Client)
class UserAdmin(admin.ModelAdmin):
    list_display = ('name', 'birthday', 'type')


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ('client', 'cep', 'street', 'number', 'district', 'city', 'uf')


@admin.register(Transporter)
class TransporterAdmin(admin.ModelAdmin):
    list_display = ('client', 'cnh', 'category_cnh')


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('client', 'transporter', 'product', 'date_order', 'total_amount', 'status')


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'value', 'weight_kg', 'photo')
