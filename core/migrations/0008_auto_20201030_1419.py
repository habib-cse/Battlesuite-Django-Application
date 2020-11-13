# Generated by Django 3.1.2 on 2020-10-30 11:19

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('core', '0007_tournamentteam'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='challenge',
            unique_together={('tournament', 'host_team', 'challenged_team')},
        ),
        migrations.AlterUniqueTogether(
            name='tournamentinvite',
            unique_together={('tournament', 'user')},
        ),
        migrations.AlterUniqueTogether(
            name='tournamentteam',
            unique_together={('tournament', 'team')},
        ),
        migrations.CreateModel(
            name='TournamentTeamUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('team', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.team')),
                ('tournament', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.tournament')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('tournament', 'team', 'user')},
            },
        ),
    ]