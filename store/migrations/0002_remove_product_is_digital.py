# Generated by Django 4.0.1 on 2023-08-17 12:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='is_digital',
        ),
    ]
