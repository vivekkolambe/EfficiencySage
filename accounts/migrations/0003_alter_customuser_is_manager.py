# Generated by Django 5.0.1 on 2024-01-14 15:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_rename_is_admin_customuser_is_manager'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='is_manager',
            field=models.BooleanField(null='true'),
        ),
    ]
