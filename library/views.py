from django.views.generic import ListView
from django.views.generic.detail import DetailView
from .models import Game, Player
from allauth.socialaccount.models import SocialAccount


class ByPlayerView(ListView):
    model = Game
    context_object_name = 'games'
    paginate_by = 12


class MyProfileView(DetailView):
    model = Player
    context_object_name = 'player'
    template_name = 'library/my_profile.html'

    def get_object(self):
        user = self.request.user
        return self.request.user.get_player()
