from django.contrib import admin
from .models import CustomUser, Client, Transporter, Order, Product
from django.contrib.auth.admin import UserAdmin


class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ['cpf', 'is_staff', 'is_active']
    search_fields = ['cpf']
    ordering = ['cpf']


admin.site.register(CustomUser, CustomUserAdmin)


@admin.register(Client)
class UserAdmin(admin.ModelAdmin):
    list_display = ('name', 'birthday', 'street', 'city')


@admin.register(Transporter)
class TransporterAdmin(admin.ModelAdmin):
    list_display = ('user', 'name', 'cnh')


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('client', 'transporter', 'date_order', 'total_amount', 'status')


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'value', 'weight_kg', 'photo')
