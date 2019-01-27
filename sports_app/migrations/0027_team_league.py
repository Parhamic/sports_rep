# Generated by Django 2.1.5 on 2019-01-16 19:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('sports_app', '0026_gameactivity_related_player'),
    ]

    operations = [
        migrations.AddField(
            model_name='team',
            name='league',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='sports_app.League'),
        ),
    ]
