# Generated by Django 5.2.3 on 2025-06-23 03:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_alter_hotelvendor_email_token'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hotel',
            name='hotel_slug',
            field=models.SlugField(max_length=225, unique=True),
        ),
    ]
