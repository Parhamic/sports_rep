from django.shortcuts import render, redirect
from .models import NewsPost, Game, Team, Player, GameActivity, Comment, League, Season
from accounts.models import User
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.utils import timezone
from django.db.models import Q
from accounts.forms import RegisterForm
from django.contrib import messages
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_text
from accounts.tokens import account_activation_token
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from accounts.models import Subscribe
import random


def main_view(request):
    try:
        num = int(request.GET.get('num'))
        if num < 1:
            raise
    except:
        num = 10
    football_posts = NewsPost.published.filter(sport='FB')[:num]
    basketball_posts = NewsPost.published.filter(sport='BB')[:num]

    today_games = Game.objects.filter(date=timezone.localdate())
    yesterday_games = Game.objects.filter(
        date=timezone.localdate()-timezone.timedelta(days=1))

    # find subscribed content
    subscribed_posts = NewsPost.objects.none()
    subscribed_today_games = Game.objects.none()
    subscribed_yesterday_games = Game.objects.none()
    if request.user.is_authenticated:
        subscribed_players = request.user.subscribes.exclude(
            player=None).select_related('player')
        subscribed_teams = request.user.subscribes.exclude(
            team=None).select_related('team')
        for player in subscribed_players:
            subscribed_posts |= NewsPost.published.filter(
                title__icontains=player.player.name)
            subscribed_posts |= NewsPost.published.filter(
                context__icontains=player.player.name)

        for team in subscribed_teams:
            subscribed_posts |= NewsPost.published.filter(
                title__icontains=team.team.name)
            subscribed_posts |= NewsPost.published.filter(
                context__icontains=team.team.name)

            subscribed_today_games |= today_games.filter(team1=team.team)
            subscribed_today_games |= today_games.filter(team2=team.team)
            subscribed_yesterday_games |= yesterday_games.filter(
                team1=team.team)
            subscribed_yesterday_games |= yesterday_games.filter(
                team2=team.team)
    return render(request, 'sports/index.html', {'football_posts': football_posts,
                                                 'basketball_posts': basketball_posts,
                                                 'subscribed_posts': subscribed_posts,
                                                 'today_games': today_games,
                                                 'yesterday_games': yesterday_games,
                                                 'subscribed_today_games': subscribed_today_games,
                                                 'subscribed_yesterday_games': subscribed_yesterday_games})


def handle_subscribes(request, **kwargs):
    context = {}
    is_subscribed = False
    if request.user.is_authenticated:
        dict_none = kwargs.copy()
        dict_none[list(dict_none.keys())[0]] = None
        subs = request.user.subscribes.values_list(
            list(kwargs.keys())[0], flat=True)
        is_subscribed = (kwargs[list(kwargs.keys())[0]].pk in subs)

    action = request.GET.get('action', '')
    if action.endswith('subscribe'):
        if is_subscribed and action == 'unsubscribe':
            # Unsubscribe
            request.user.subscribes.filter(**kwargs).delete()
            is_subscribed = False
        if not is_subscribed and action == 'subscribe':
            # Subscribe
            Subscribe.objects.create(user=request.user, **kwargs)
            is_subscribed = True
    return is_subscribed


class LeagueDetailView(DetailView):
    model = Season
    template_name = 'sports/leaguealpha.html'


class LeaguesListView(ListView):
    model = Season
    template_name = 'sports/leagues.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        q = self.request.GET.get('q', '')
        if q != '':
            words = []
            num = None
            for word in q.split():
                if word.isnumeric():
                    num = int(word)
                else:
                    words.append(word)
            q = ' '.join(words)
            q = q.strip()
            print('searching for : ' + q)
            context['seasons'] = Season.objects.filter(
                league__title__icontains=q)
            if num:
                context['seasons'] = context['seasons'].filter(
                    year__icontains=num)
        else:
            context['seasons'] = Season.objects.all()
        return context


class PostDetailView(DetailView):
    model = NewsPost
    template_name = 'sports/newsalpha.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comments'] = self.get_object().comments.filter(active=True)
        return context

    def post(self, request, *args, **kwargs):
        try:
            text = request.POST['text']
            Comment.objects.create(
                post=self.get_object(), author=request.user.username, text=text, active=True)
        except:
            pass
        # reload the page
        return redirect(self.get_object())


class PlayerDetailView(DetailView):
    model = Player
    template_name = 'sports/player.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        player = self.get_object()
        context['is_subscribed'] = handle_subscribes(
            self.request, player=player)

        # Calculate stats
        seasons = {}
        player_seasons = player.team.league.seasons.all()
        for season in player_seasons:
            seasons[str(season)] = {}
            player_season_acitivities = GameActivity.objects.filter(game__season=season,
                                                                    related_player=player)
            seasons[str(season)]['goals'] = player_season_acitivities.filter(
                title='goal').count()
            seasons[str(season)]['assists'] = player_season_acitivities.filter(
                title='assist').count()
            seasons[str(season)]['yellow_cards'] = player_season_acitivities.filter(
                title='yellow card').count()
            seasons[str(season)]['red_cards'] = player_season_acitivities.filter(
                title='red card').count()
        context['seasons'] = seasons

        # Find related news
        filter_by = self.request.GET.get('filter_by', 'title')
        if filter_by == 'title':
            related_news = NewsPost.published.filter(
                title__icontains=player.name)
        else:
            related_news = NewsPost.published.filter(
                context__icontains=player.name)
        context['related_news'] = related_news
        return context


class GameDetailView(DetailView):
    model = Game
    template_name = 'sports/footballgame.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        game = self.get_object()

        # Find related news
        context['related_news'] = NewsPost.objects.filter(
            state='GR', game=game)
        return context


class TeamDetailView(DetailView):
    model = Team
    template_name = 'sports/teamalpha.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        team = self.get_object()
        context['is_subscribed'] = handle_subscribes(
            self.request, team=team)
        # Find games
        context['games'] = Game.objects.filter(Q(team1=team) | Q(team2=team))

        # Find related news
        filter_by = self.request.GET.get('filter_by', 'title')

        if filter_by == 'title':
            related_news = NewsPost.published.filter(
                title__icontains=team.name)
            for player in team.players.all():
                related_news = NewsPost.published.filter(
                    title__icontains=player.name)
        else:
            related_news = NewsPost.published.filter(
                context__icontains=team.name)
            for player in team.players.all():
                related_news |= NewsPost.published.filter(
                    context__icontains=player.name)
        context['related_news'] = related_news
        return context


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.email_confirmed = True
        user.save()
        login(request, user, backend='django.contrib.auth.backends.ModelBackend')
        return redirect('main_view')
    else:
        return render(request, 'account_activation_invalid.html')


def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            subject = 'Activate Your MySite Account'
            message = render_to_string('account_activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': force_text(urlsafe_base64_encode(force_bytes(user.pk))),
                'token': account_activation_token.make_token(user),
            })
            user.email_user(subject, message)
            messages.success(request, 'Please confirm your email.')
            return render(request, 'signup.html', {'form': form})
    else:
        form = RegisterForm()
    return render(request, 'signup.html', {'form': form})


def random_password():
    pw = ''
    for i in range(random.randint(6, 12)):
        pw += chr(random.randint(ord('A'), ord('z')))
    return pw


def reset_password_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        try:
            user = User.objects.get(username=username)
            new_password = random_password()
            user.set_password(new_password)
            user.save()
            current_site = get_current_site(request)
            message = render_to_string('reset_password_email.html', {
                'user': user,
                'domain': current_site.domain,
                'new_password': new_password
            })
            user.email_user('Password reset', message)
            messages.success(
                request, 'Your new password has been emailed to you')
        except:
            messages.error(request, 'Username not found')
    return render(request, 'reset_password.html')


def logout_view(request):
    logout(request)
    return redirect('main_view')
