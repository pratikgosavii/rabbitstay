# Generated by Django 5.1.4 on 2025-06-09 09:27

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('masters', '0024_remove_vaccination_image'),
    ]

    operations = [
        migrations.CreateModel(
            name='hotel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('address', models.TextField()),
                ('city', models.CharField(max_length=100)),
                ('star_rating', models.IntegerField()),
                ('price_per_night', models.DecimalField(decimal_places=2, max_digits=10)),
                ('includes_taxes', models.BooleanField(default=True)),
                ('free_cancellation_till', models.DateField(blank=True, null=True)),
                ('free_breakfast', models.BooleanField(default=False)),
                ('overall_rating', models.DecimalField(blank=True, decimal_places=1, max_digits=2, null=True)),
                ('total_reviews', models.IntegerField(default=0)),
                ('main_image', models.ImageField(blank=True, null=True, upload_to='hotels/')),
                ('is_featured', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('amenities', models.ManyToManyField(blank=True, to='masters.amenity')),
            ],
        ),
        migrations.CreateModel(
            name='HotelImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='hotel_gallery/')),
                ('is_primary', models.BooleanField(default=False)),
                ('hotel', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='hotel.hotel')),
            ],
        ),
    ]
