# Generated by Django 5.0.2 on 2024-02-15 17:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='client',
            name='type',
            field=models.CharField(choices=[('client', 'Client'), ('transporter', 'Transporter')], max_length=40),
        ),
    ]
