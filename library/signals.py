from datetime import datetime

from allauth.socialaccount.signals import pre_social_login
from django.dispatch import receiver

from library.models import Player


@receiver(pre_social_login)
def upsert_player_from_login(request, sociallogin, **kwargs):
    if sociallogin.account.provider == "steam":
        payload = sociallogin.account.extra_data

        player_obj, created = Player.objects.update_or_create(
            steamid=payload["steamid"],
            defaults={
                "nickname": payload["personaname"],
                "real_name": payload["realname"],
                "profile_url": payload["profileurl"],
                "avatar_url": payload["avatar"],
                "avatar_m_url": payload["avatarmedium"],
                "avatar_f_url": payload["avatarfull"],
                "country_code": payload["loccountrycode"],
                "creation_date": datetime.fromtimestamp(payload["timecreated"]),
            },
        )
