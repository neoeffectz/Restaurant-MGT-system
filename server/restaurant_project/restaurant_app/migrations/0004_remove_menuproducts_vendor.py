# Generated by Django 4.2.6 on 2023-10-27 18:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('restaurant_app', '0003_remove_customuser_role'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='menuproducts',
            name='vendor',
        ),
    ]
