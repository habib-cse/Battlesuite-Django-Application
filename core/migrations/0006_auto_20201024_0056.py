# Generated by Django 3.1.2 on 2020-10-23 21:56

import core.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('core', '0005_tournament_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='team',
            name='icon',
            field=models.ImageField(upload_to=core.models.team_based_upload_to),
        ),
        migrations.CreateModel(
            name='TournamentInvite',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tournament', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.tournament')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]