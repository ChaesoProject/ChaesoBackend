# Generated by Django 5.0.2 on 2024-03-21 19:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0012_remove_order_products_remove_order_quantity'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='products',
            field=models.ManyToManyField(to='core.product'),
        ),
    ]
