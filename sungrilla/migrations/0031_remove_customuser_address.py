# Generated by Django 5.0.6 on 2024-07-10 09:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sungrilla', '0030_customuser_alter_actionlog_user_alter_cart_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customuser',
            name='address',
        ),
    ]
