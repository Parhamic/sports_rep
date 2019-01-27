# Generated by Django 2.1.5 on 2019-01-16 19:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('sports_app', '0025_auto_20190116_2301'),
    ]

    operations = [
        migrations.AddField(
            model_name='gameactivity',
            name='related_player',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='activities', to='sports_app.Player'),
        ),
    ]
