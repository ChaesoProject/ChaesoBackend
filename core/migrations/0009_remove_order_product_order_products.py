# Generated by Django 5.0.2 on 2024-03-07 19:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0008_alter_order_date_order_alter_order_status_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='product',
        ),
        migrations.AddField(
            model_name='order',
            name='products',
            field=models.ManyToManyField(to='core.product'),
        ),
    ]
