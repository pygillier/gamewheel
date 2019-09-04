from datetime import datetime

from constance import config
from django.core.management.base import BaseCommand
from steam.webapi import WebAPI

from library.models import Game
from library.models import GameStat
from library.models import Player


class Command(BaseCommand):
    help = "Import given user's library into database"

    def add_arguments(self, parser):
        parser.add_argument("nickname", type=str)

    def handle(self, *args, **options):
        api = WebAPI(key=config.STEAM_API_TOKEN)

        res = api.ISteamUser.ResolveVanityURL(vanityurl=options["nickname"], url_type=1)

        if res["response"]["success"] == 1:
            steamid = res["response"]["steamid"]
            self.stdout.write(self.style.SUCCESS("user found: %s" % steamid))
        else:
            self.stdout.write("User not found, cancelling")
            return -1

        # Get user details
        user = api.ISteamUser.GetPlayerSummaries(steamids=steamid)["response"]

        player = user["players"][0]
        player_obj, created = Player.objects.update_or_create(
            steamid=player["steamid"],
            defaults={
                "nickname": player["personaname"],
                "real_name": player["realname"],
                "profile_url": player["profileurl"],
                "avatar_url": player["avatar"],
                "avatar_m_url": player["avatarmedium"],
                "avatar_f_url": player["avatarfull"],
                "country_code": player["loccountrycode"],
                "creation_date": datetime.fromtimestamp(player["timecreated"]),
            },
        )
        if created:
            self.stdout.write("User created into DB")
        else:
            self.stdout.write("User found & updated in DB")

        # Get games
        games = api.IPlayerService.GetOwnedGames(
            steamid=steamid,
            include_appinfo=True,
            include_played_free_games=True,
            appids_filter=None,
        )["response"]

        self.stdout.write("Got %s games, upserting." % games["game_count"])

        for game in games["games"]:
            game_obj, created = Game.objects.update_or_create(
                appid=game["appid"],
                defaults={
                    "name": game["name"],
                    "icon_id": game["img_icon_url"],
                    "logo_id": game["img_logo_url"],
                },
            )

            if created:
                self.stdout.write("Game %s created in DB" % game["name"])
            else:
                self.stdout.write("Game %s updated in DB" % game["name"])

            # User's stat on game
            stat, created = GameStat.objects.update_or_create(
                player=player_obj,
                game=game_obj,
                defaults={"playtime": game["playtime_forever"]},
            )
