# Generated by Django 4.0.1 on 2022-06-15 14:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0028_remove_address_order_order_address'),
    ]

    operations = [
        migrations.AlterField(
            model_name='address',
            name='zip',
            field=models.CharField(default='string', max_length=200),
            preserve_default=False,
        ),
    ]
