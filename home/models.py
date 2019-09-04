from django.contrib.auth.models import AbstractUser
from library.models import Player
from allauth.socialaccount.models import SocialAccount


class User(AbstractUser):

    def get_player(self):
        steam_account = SocialAccount.objects.filter(user=self, provider='steam').first()

        return Player.objects.filter(steamid=steam_account.uid).first()