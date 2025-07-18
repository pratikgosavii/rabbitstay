# Generated by Django 5.1.4 on 2025-06-24 12:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0006_alter_hotelbooking_hotel_earning'),
    ]

    operations = [
        migrations.AddField(
            model_name='hotelbooking',
            name='tcs_amount',
            field=models.DecimalField(decimal_places=2, default=0.0, help_text='1% TCS on subtotal', max_digits=10),
        ),
        migrations.AddField(
            model_name='hotelbooking',
            name='tds_amount',
            field=models.DecimalField(decimal_places=2, default=0.0, help_text='1% TDS on subtotal', max_digits=10),
        ),
    ]
