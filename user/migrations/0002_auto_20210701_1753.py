# Generated by Django 3.2.4 on 2021-07-01 08:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='member',
            name='user_phone',
            field=models.CharField(max_length=20, unique=True),
        ),
        migrations.AlterModelTable(
            name='member',
            table='member',
        ),
    ]