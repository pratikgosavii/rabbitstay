# Generated by Django 5.1.4 on 2025-06-30 22:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hotel', '0019_alter_hotel_profit_margin'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hotel',
            name='star_rating',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
