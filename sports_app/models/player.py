from django.db import models
from .team import Team
from django.utils.text import slugify
from django.core.exceptions import ValidationError
from django.urls import reverse


class Player(models.Model):
    SPORTS = (('FB', 'Football'),
              ('BB', 'Basketball'))
    sport = models.CharField(max_length=2, choices=SPORTS)
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(blank=True, unique=True)
    age = models.PositiveIntegerField()
    nation = models.CharField(max_length=20)
    height = models.PositiveIntegerField(default=0)
    weight = models.PositiveIntegerField(default=0)
    team = models.ForeignKey(Team,
                             blank=True, null=True, on_delete=models.SET_NULL, related_name='players')
    role = models.CharField(blank=True, max_length=32)
    image = models.ImageField(upload_to='player_pictures')

    def clean(self):
        if self.team and self.team.sport != self.sport:
            raise ValidationError('Team\'s sport must be the same as player')

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        create_info = False
        if not self.pk:
            create_info = True
            if self.team.sport == 'FB':
                info = FootballPlayerInfo()
            else:
                info = BasketballPlayerInfo()
        super(Player, self).save(*args, **kwargs)
        if create_info:
            info.player = self
            info.save()

    def get_absolute_url(self):
        return reverse('player_view', kwargs={'slug': self.slug})

    def __str__(self):
        return self.name


class FootballPlayerInfo(models.Model):
    player = models.OneToOneField(Player,
                                  related_name='football_info', on_delete=models.CASCADE)


class BasketballPlayerInfo(models.Model):
    player = models.OneToOneField(Player,
                                  related_name='basketball_info', on_delete=models.CASCADE)
