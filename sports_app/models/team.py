from django.db import models
from django.utils.text import slugify
from django.urls import reverse
from .league import League


class Team(models.Model):
    SPORTS = (('FB', 'Football'),
              ('BB', 'Basketball'))
    sport = models.CharField(max_length=2, choices=SPORTS)
    name = models.CharField(max_length=64, unique=True)
    league = models.ForeignKey(League,
                               null=True, on_delete=models.SET_NULL, related_name='teams')
    image = models.ImageField(
        null=True, blank=True, upload_to='team_pictures')
    slug = models.SlugField(blank=True, unique=True)

    # season info
    num_games = models.PositiveIntegerField(default=0)
    num_wins = models.PositiveIntegerField(default=0)
    num_losts = models.PositiveIntegerField(default=0)
    num_points = models.PositiveIntegerField(default=0)
    num_draws = models.PositiveIntegerField(default=0)
    num_gf = models.PositiveIntegerField(default=0)
    num_ga = models.PositiveIntegerField(default=0)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super(Team, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('team_view', kwargs={'slug': self.slug})

    def __str__(self):
        return self.name
