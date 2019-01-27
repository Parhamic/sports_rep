from django.db import models
from django.contrib.auth.models import AbstractUser
from sports_app.models import Game, Team, Player


class User(AbstractUser):
    REQUIRED_FIELDS = ['email', 'first_name', 'last_name']
    email_confirmed = models.BooleanField(default=False)


class Subscribe(models.Model):
    user_related_to = models.ForeignKey(User,
                             related_name='subscribes', on_delete=models.CASCADE)
    team = models.ForeignKey(Team,
                             null=True, blank=True, on_delete=models.CASCADE)
    game = models.ForeignKey(Game,
                             null=True, blank=True, on_delete=models.CASCADE)
    player = models.ForeignKey(Player,
                               null=True, blank=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username
