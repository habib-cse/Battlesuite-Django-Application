# Generated by Django 3.1.2 on 2020-11-09 18:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0016_auto_20201109_1436'),
    ]

    operations = [
        migrations.AddField(
            model_name='loadingscreenadmin',
            name='ready',
            field=models.BooleanField(default=False),
        ),
    ]
