# Generated by Django 5.2.3 on 2025-06-24 11:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_hotelvendor_business_name'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='hoteluser',
            options={},
        ),
        migrations.AlterModelOptions(
            name='hotelvendor',
            options={},
        ),
        migrations.AlterModelTable(
            name='hoteluser',
            table='hotel_user',
        ),
        migrations.AlterModelTable(
            name='hotelvendor',
            table='hotel_vendor',
        ),
    ]
