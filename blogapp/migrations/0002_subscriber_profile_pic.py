# Generated by Django 5.0.1 on 2024-01-23 07:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blogapp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='subscriber',
            name='profile_pic',
            field=models.ImageField(blank=True, default='default.webp', null=True, upload_to=''),
        ),
    ]
