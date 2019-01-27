from django.db import models
from .team import Team
from .player import Player
from .league import Season
from django.core.exceptions import ValidationError
from django.urls import reverse
from django.utils.text import slugify, mark_safe
from django.utils import timezone


class Game(models.Model):
    STATES = (('NB', 'Not finished'),
              ('TIE', 'Tie'),
              ('WIN', 'Win'))
    season = models.ForeignKey(Season,
                               related_name='games', on_delete=models.CASCADE)
    team1 = models.ForeignKey(Team,
                              on_delete=models.CASCADE, related_name='games1')
    team2 = models.ForeignKey(Team,
                              on_delete=models.CASCADE, related_name='games2')
    players = models.ManyToManyField(Player, related_name='games')
    score_1 = models.PositiveIntegerField(default=0)
    score_2 = models.PositiveIntegerField(default=0)
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    state = models.CharField(max_length=3, choices=STATES, default='NB')
    winner = models.ForeignKey(Team, null=True, blank=True,
                               on_delete=models.CASCADE, related_name='wins')

    def save(self, *args, **kwargs):
        create_info = False
        if not self.pk:
            create_info = True
            if self.team1.sport == 'FB':
                info = FootballGameInfo()
            else:
                info = BasketballGameInfo()
        super(Game, self).save(*args, **kwargs)
        if create_info:
            info.game = self
            info.save()

    def get_absolute_url(self):
        return reverse('game_view', kwargs={'pk': self.pk})

    def get_info(self):
        if self.state != 'NB':
            if self.winner:
                return 'Winner: {}'.format(self.winner)
            else:
                return 'Tie'
        else:
            if self.date != timezone.localtime().date() or not(self.start_time <= timezone.localtime().time() and self.end_time > timezone.localtime().time()):
                return 'Upcoming ({} {})'.format(self.date.strftime('%Y-%m-%d'), self.start_time.strftime('%H:%m'))
            else:
                return 'Ongoing'

    def clean(self):
        if self.team1 == self.team2:
            raise ValidationError('Teams cant be the same')
        if self.team1.sport != self.team2.sport:
            raise ValidationError('Teams cant be from different sports')
        if self.end_time < self.start_time:
            raise ValidationError('End time cant be less than start time')
        if self.winner and self.winner != self.team1 and self.winner != self.team2:
            raise ValidationError('Winner must be one of the two teams')
        if self.team1.league != self.team2.league:
            raise ValidationError('Teams must be at same league')
        if self.season.league != self.team1.league:
            raise ValidationError('The season must belong to teams\' league')

    def __str__(self):
        return '{} vs {}'.format(self.team1.name, self.team2.name)


class Media(models.Model):
    game = models.ForeignKey(
        Game, on_delete=models.CASCADE, related_name='media')
    image = models.ImageField()


class FootballGameInfo(models.Model):
    game = models.OneToOneField(Game,
                                null=True, on_delete=models.SET_NULL, parent_link=True, related_name='football_info')

    goals_1 = models.PositiveIntegerField(default=0)
    possession_1 = models.PositiveIntegerField(default=0)
    shots_1 = models.PositiveIntegerField(default=0)
    shots_on_target_1 = models.PositiveIntegerField(default=0)
    yellow_cards_1 = models.PositiveIntegerField(default=0)
    red_cards_1 = models.PositiveIntegerField(default=0)
    corners_1 = models.PositiveIntegerField(default=0)
    offsides_1 = models.PositiveIntegerField(default=0)
    fouls_1 = models.PositiveIntegerField(default=0)

    goals_2 = models.PositiveIntegerField(default=0)
    possession_2 = models.PositiveIntegerField(default=0)
    shots_2 = models.PositiveIntegerField(default=0)
    shots_on_target_2 = models.PositiveIntegerField(default=0)
    yellow_cards_2 = models.PositiveIntegerField(default=0)
    red_cards_2 = models.PositiveIntegerField(default=0)
    corners_2 = models.PositiveIntegerField(default=0)
    offsides_2 = models.PositiveIntegerField(default=0)
    fouls_2 = models.PositiveIntegerField(default=0)


class BasketballGameInfo(models.Model):
    game = models.OneToOneField(Game,
                                null=True, on_delete=models.SET_NULL, parent_link=True, related_name='basketball_info')
    score_1 = models.PositiveIntegerField(default=0)
    q1_1 = models.PositiveIntegerField(default=0)
    q2_1 = models.PositiveIntegerField(default=0)
    q3_1 = models.PositiveIntegerField(default=0)
    q4_1 = models.PositiveIntegerField(default=0)
    threepoint_1 = models.PositiveIntegerField(default=0)
    twopoint_1 = models.PositiveIntegerField(default=0)
    penalty_1 = models.PositiveIntegerField(default=0)
    fouls_1 = models.PositiveIntegerField(default=0)
    rebound_1 = models.PositiveIntegerField(default=0)

    score_2 = models.PositiveIntegerField(default=0)
    q1_2 = models.PositiveIntegerField(default=0)
    q2_2 = models.PositiveIntegerField(default=0)
    q3_2 = models.PositiveIntegerField(default=0)
    q4_2 = models.PositiveIntegerField(default=0)
    threepoint_2 = models.PositiveIntegerField(default=0)
    twopoint_2 = models.PositiveIntegerField(default=0)
    penalty_2 = models.PositiveIntegerField(default=0)
    fouls_2 = models.PositiveIntegerField(default=0)
    rebound_2 = models.PositiveIntegerField(default=0)


class GameActivity(models.Model):
    game = models.ForeignKey(Game,
                             related_name='activities', on_delete=models.CASCADE)
    title = models.CharField(max_length=30)
    related_player = models.ForeignKey(Player,
                                       blank=True, null=True, on_delete=models.SET_NULL, related_name='activities')
    description = models.TextField(blank=True)
