from django.db import models
from django.urls import reverse


class League(models.Model):
    title = models.CharField(max_length=30, unique=True)

    def __str__(self):
        return '{}'.format(self.title)


class Season(models.Model):
    league = models.ForeignKey(League,
                               related_name='seasons', on_delete=models.CASCADE)
    year = models.CharField(max_length=10)

    def get_absolute_url(self):
        return reverse('league_view', kwargs={'pk': self.pk})

    def __str__(self):
        return '{} - {}'.format(self.league.title, self.year)
