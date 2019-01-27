from .models import NewsPost, Player, Team, Game
from django.db.models.signals import pre_delete, post_delete
from django.dispatch import receiver


@receiver(pre_delete, sender=NewsPost)
@receiver(pre_delete, sender=Team)
@receiver(pre_delete, sender=Player)
def on_delete(sender, **kwargs):
    instance = kwargs['instance']
    if instance.image:
        instance.image.delete(save=False)


@receiver(pre_delete, sender=Game)
def on_game_delete(sender, **kwargs):
    instance = kwargs['instance']
    if hasattr(instance, 'basketball_info') and instance.basketball_info:
        instance.basketball_info.delete()
    if hasattr(instance, 'football_info') and instance.football_info:
        instance.football_info.delete()
