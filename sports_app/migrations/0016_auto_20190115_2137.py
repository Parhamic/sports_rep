# Generated by Django 2.1.5 on 2019-01-15 18:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('sports_app', '0015_remove_game_slug'),
    ]

    operations = [
        migrations.AddField(
            model_name='team',
            name='image',
            field=models.ImageField(default=None, upload_to='team_pictures'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='basketballplayerinfo',
            name='player',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='basketball_info', to='sports_app.Player'),
        ),
        migrations.AlterField(
            model_name='footballplayerinfo',
            name='player',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='football_info', to='sports_app.Player'),
        ),
        migrations.AlterField(
            model_name='player',
            name='team',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='players', to='sports_app.Team'),
        ),
    ]
