# Generated by Django 3.2.4 on 2021-08-02 17:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('messenger_backend', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='read',
            field=models.BooleanField(default=False),
        ),
    ]
