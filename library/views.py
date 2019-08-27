from django.views.generic import ListView, RedirectView
from django.views.generic.detail import DetailView
from django.shortcuts import get_object_or_404
from .models import Game, Player, GameStat


class ByPlayerView(ListView):
    model = Game
    context_object_name = 'games'
    paginate_by = 12

    def get_queryset(self):
        player = self.request.user.get_player()
        return Game.objects.filter(player=player)


class MyProfileView(DetailView):
    model = Player
    context_object_name = 'player'
    template_name = 'library/my_profile.html'

    def get_object(self, queryset=None):
        return self.request.user.get_player()


class ImportLibraryView(RedirectView):
    permanent = False
    pattern_name = 'library:my_profile'

    def get_redirect_url(self, *args, **kwargs):
        player = self.request.user.get_player()
        Player.objects.import_library(player)
        return super().get_redirect_url(*args, **kwargs)


class MarkAsPlayingView(RedirectView):
    permanent = False
    query_string = False
    pattern_name = 'library:my_profile'

    def get_redirect_url(self, *args, **kwargs):
        game = get_object_or_404(
            GameStat,
            player=self.request.user.get_player(),
            game_id=kwargs['appid'])
        game.play()
        return super().get_redirect_url()

class MarkAsFinishedView(RedirectView):
    permanent = False
    query_string = False
    pattern_name = 'library:my_profile'

    def get_redirect_url(self, *args, **kwargs):
        game = get_object_or_404(
            GameStat,
            player=self.request.user.get_player(),
            game_id=kwargs['appid'])
        game.finish()
        return super().get_redirect_url()
