import xml.etree.ElementTree as ET
from datetime import datetime

import requests
from allauth.exceptions import ImmediateHttpResponse
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from django.contrib.sites.shortcuts import get_current_site
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy

from library.models import Group
from library.models import Player


class SteamWithGroupCheckAdapter(DefaultSocialAccountAdapter):
    def __init__(self, request=None):
        super().__init__(request)

    def is_valid_membership(self, steam_id):
        """
        Check is given steam_id belongs to current_site groups.
        :param steam_id: steamID 64 to check
        :return: boolean
        """

        # Load groups from user profile if possible.
        url = f"https://steamcommunity.com/profiles/{steam_id}?xml=1"
        r = requests.get(url=url)

        try:
            payload = ET.fromstring(r.text)

            # Make sure we have a valid XML tree
            assert payload.tag == "profile"

            gids = [g.text for g in payload.findall("./groups/group/groupID64")]

            # Check if we have an intersection
            membership = Group.objects.filter(
                site=get_current_site(self.request), group_id__in=gids
            )

            if membership.count() > 0:
                return True

        except AssertionError:
            # Not a valid XML, returning...
            return False

        # Always return False by default.
        return False

    def pre_social_login(self, request, sociallogin):
        if sociallogin.account.provider == "steam":

            payload = sociallogin.account.extra_data

            if not self.is_valid_membership(payload["steamid"]):
                uri = reverse_lazy("library:not-in-groups")
                raise ImmediateHttpResponse(HttpResponseRedirect(uri))

            # User is logged-in an in groups, let's upsert it
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

            if created:
                print("User created into DB")
            else:
                print("User found & updated in DB")
