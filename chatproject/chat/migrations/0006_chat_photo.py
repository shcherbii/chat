# Generated by Django 4.2.9 on 2024-02-13 15:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0005_alter_chatmassages_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='chat',
            name='photo',
            field=models.ImageField(blank=True, upload_to='chats/%Y/%m/%d'),
        ),
    ]