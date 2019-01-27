# Generated by Django 2.1.5 on 2019-01-15 10:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sports_app', '0003_newspost_state'),
    ]

    operations = [
        migrations.CreateModel(
            name='FootballPlayer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('age', models.PositiveIntegerField()),
                ('role', models.CharField(max_length=32)),
                ('picture', models.ImageField(upload_to='player_pictures')),
            ],
        ),
    ]