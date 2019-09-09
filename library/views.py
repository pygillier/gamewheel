from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import get_object_or_404
from django.views.generic import ListView
from django.views.generic import RedirectView
from django.views.generic import TemplateView
from django.views.generic.detail import DetailView

from .models import Game
from .models import GameStat
from .models import Group
from .models import Player


class NotInGroupsView(TemplateView):
    template_name = "library/not_in_groups.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["groups"] = Group.objects.filter(
            site=get_current_site(self.request)
        ).all()

        return context


class ByPlayerView(ListView):
    model = Game
    context_object_name = "games"
    paginate_by = 12

    def get_queryset(self):
        player = self.request.user.get_player()
        return Game.objects.filter(player=player)


class MyProfileView(DetailView):
    model = Player
    context_object_name = "player"
    template_name = "library/my_profile.html"

    def get_object(self, queryset=None):
        return self.request.user.get_player()


class ImportLibraryView(RedirectView):
    permanent = False
    pattern_name = "library:my_profile"

    def get_redirect_url(self, *args, **kwargs):
        player = self.request.user.get_player()
        Player.objects.import_library(player)
        return super().get_redirect_url(*args, **kwargs)


class MarkAsPlayingView(RedirectView):
    permanent = False
    query_string = False
    pattern_name = "library:my_profile"

    def get_redirect_url(self, *args, **kwargs):
        game = get_object_or_404(
            GameStat, player=self.request.user.get_player(), game_id=kwargs["appid"]
        )
        game.play()
        return super().get_redirect_url()


class MarkAsFinishedView(RedirectView):
    permanent = False
    query_string = False
    pattern_name = "library:my_profile"

    def get_redirect_url(self, *args, **kwargs):
        game = get_object_or_404(
            GameStat, player=self.request.user.get_player(), game_id=kwargs["appid"]
        )
        game.finish()
        return super().get_redirect_url()
