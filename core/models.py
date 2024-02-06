from django.db import models


class User(models.Model):
    name = models.CharField(max_length=40)
    cpf = models.CharField(max_length=14)
    birthday = models.DateField()
    type = models.CharField(max_length=40)

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def __str__(self):
        return f'{self.name}, {self.cpf}'


class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
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
        return f'{self.user}, {self.street}'


class Transporter(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    cnh = models.CharField(max_length=20)
    category_cnh = models.CharField(max_length=5)

    class Meta:
        verbose_name = 'Transporter'
        verbose_name_plural = 'Transporters'

    def __str__(self):
        return f'{self.user}, {self.cnh}'
    

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    transporter = models.ForeignKey(Transporter, on_delete=models.CASCADE)
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    date_order = models.DateField()
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=50)

    class Meta:
        verbose_name = 'Order'
        verbose_name_plural = 'Orders'

    def __str__(self):
        return f'{self.user}, {self.transporter}, {self.total_amount}'


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
