# Generated by Django 3.2 on 2024-10-09 08:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0006_alter_user_is_subscribed'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='avatar',
            field=models.ImageField(blank=True, null=True, upload_to='users/avatars/', verbose_name='Фото профиля'),
        ),
    ]