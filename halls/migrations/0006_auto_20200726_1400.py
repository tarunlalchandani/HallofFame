# Generated by Django 3.0.8 on 2020-07-26 08:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('halls', '0005_auto_20200725_1140'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='is_verified',
        ),
        migrations.AddField(
            model_name='profile',
            name='email_confirmed',
            field=models.BooleanField(default=False),
        ),
    ]
