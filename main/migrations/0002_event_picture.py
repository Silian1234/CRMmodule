# Generated by Django 5.0.6 on 2024-12-03 10:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='picture',
            field=models.ImageField(blank=True, null=True, upload_to='event_pictures/'),
        ),
    ]
