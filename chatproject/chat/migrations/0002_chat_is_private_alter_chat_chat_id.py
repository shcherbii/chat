# Generated by Django 4.2.9 on 2024-02-11 21:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='chat',
            name='is_private',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='chat',
            name='chat_id',
            field=models.CharField(max_length=39, null=True, unique=True),
        ),
    ]
