# Generated by Django 5.0.1 on 2024-01-23 08:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blogapp', '0002_subscriber_profile_pic'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subscriber',
            name='profile_pic',
            field=models.ImageField(blank=True, default='images/default.webp', null=True, upload_to=''),
        ),
    ]