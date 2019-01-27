from django.contrib import admin
from .models import NewsPost, Game, Team, Player, League, Comment
from .models.league import Season
from .models.game import FootballGameInfo, BasketballGameInfo, GameActivity, Media
from django.contrib.auth.models import Group


class FootballInfoAdmin(admin.TabularInline):
    model = FootballGameInfo
    extra = 0


class BasketballInfoAdmin(admin.TabularInline):
    model = BasketballGameInfo
    extra = 0


class GameActivityAdmin(admin.StackedInline):
    model = GameActivity
    extra = 0


class MediaAdmin(admin.StackedInline):
    model = Media
    extra = 0


class SeasonAdmin(admin.StackedInline):
    model = Season
    extra = 0


@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    inlines = [FootballInfoAdmin, BasketballInfoAdmin,
               GameActivityAdmin, MediaAdmin]


@admin.register(League)
class LeagueAdmin(admin.ModelAdmin):
    inlines = [SeasonAdmin]


admin.site.unregister(Group)
admin.site.register(NewsPost)
admin.site.register(Comment)
admin.site.register(Team)
admin.site.register(Player)
