# Generated by Django 4.2.13 on 2024-05-17 03:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('yingfu', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='user',
            managers=[
            ],
        ),
        migrations.AlterField(
            model_name='user',
            name='phone',
            field=models.CharField(max_length=20, verbose_name='手机号'),
        ),
    ]
