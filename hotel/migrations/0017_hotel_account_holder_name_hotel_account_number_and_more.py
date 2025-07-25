# Generated by Django 5.1.4 on 2025-06-30 07:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hotel', '0016_hotel_profit_margin'),
    ]

    operations = [
        migrations.AddField(
            model_name='hotel',
            name='account_holder_name',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='hotel',
            name='account_number',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
        migrations.AddField(
            model_name='hotel',
            name='bank_document',
            field=models.FileField(blank=True, help_text='Upload Cancelled Cheque or Bank Passbook (Image/PDF)', null=True, upload_to='hotel_docs/bank_docs/'),
        ),
        migrations.AddField(
            model_name='hotel',
            name='bank_name',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='hotel',
            name='category',
            field=models.CharField(choices=[('Budget', 'Budget'), ('Mid_range', 'Mid-range'), ('Premium', 'Premium'), ('Boutique', 'Boutique')], default='Budget', max_length=50),
        ),
        migrations.AddField(
            model_name='hotel',
            name='gst_certificate',
            field=models.FileField(blank=True, help_text='Upload GST Certificate (PDF/Image)', null=True, upload_to='hotel_docs/gst_certificates/'),
        ),
        migrations.AddField(
            model_name='hotel',
            name='gst_number',
            field=models.CharField(blank=True, help_text='GST Number (15 characters, e.g., 29ABCDE1234F2Z5)', max_length=15, null=True),
        ),
        migrations.AddField(
            model_name='hotel',
            name='ifsc_code',
            field=models.CharField(blank=True, max_length=15, null=True),
        ),
        migrations.AddField(
            model_name='hotel',
            name='no_of_rooms',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='hotel',
            name='pan_number',
            field=models.CharField(blank=True, help_text='PAN Card Number (optional)', max_length=10, null=True),
        ),
    ]
