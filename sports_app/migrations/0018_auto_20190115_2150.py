# Generated by Django 2.1.5 on 2019-01-15 18:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('sports_app', '0017_auto_20190115_2138'),
    ]

    operations = [
        migrations.AlterField(
            model_name='footballgameinfo',
            name='game',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, parent_link=True, related_name='football_info', to='sports_app.Game'),
        ),
    ]