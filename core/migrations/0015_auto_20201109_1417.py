# Generated by Django 3.1.2 on 2020-11-09 11:17

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('core', '0014_auto_20201109_1405'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='loadingscreenadmin',
            unique_together={('loadingscreen', 'admin')},
        ),
    ]
