# Generated by Django 5.1.4 on 2025-06-24 01:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0005_hotelbooking_commission_amount_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hotelbooking',
            name='hotel_earning',
            field=models.DecimalField(decimal_places=2, default=5.0, max_digits=10),
        ),
    ]
