from datetime import datetime
from enum import Enum

from allauth.socialaccount.models import SocialApp
from django.contrib.sites.models import Site
from django.db import models
from django.db.models import Count
from django.db.models import Max
from django.db.models import Min
from django_random_queryset import strategies
from steam.webapi import WebAPI


class PlayChoice(Enum):
    NONE = "unknown"
    PLAYING = "playing"
    FINISHED = "finished"


class RandomQuerySet(models.query.QuerySet):
    def random(self, amount=1):
        aggregates = self.aggregate(
            min_id=Min("appid"), max_id=Max("appid"), count=Count("appid")
        )

        if not aggregates["count"]:
            return self.none()

        if aggregates["count"] <= amount:
            return self.all()

        if (aggregates["max_id"] - aggregates["min_id"]) + 1 == aggregates["count"]:
            return self.filter(
                appid__in=strategies.min_max(
                    amount,
                    aggregates["min_id"],
                    aggregates["max_id"],
                    aggregates["count"],
                )
            )

        try:
            selected_ids = strategies.min_max_count(
                amount, aggregates["min_id"], aggregates["max_id"], aggregates["count"]
            )
        except strategies.SmallPopulationSize:
            selected_ids = self.values_list("appid", flat=True)

        assert len(selected_ids) > amount
        return self.filter(appid__in=selected_ids).order_by("?")[:amount]


class GameManager(models.Manager):
    def random(self, *args, **kwargs):
        return self.__get_queryset().random(*args, **kwargs)

    def get_queryset(self):
        return RandomQuerySet(self.model)


class Game(models.Model):

    # Custom manager to have a clean random selector
    objects = GameManager()

    appid = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=255)

    icon_id = models.CharField(max_length=40)
    logo_id = models.CharField(max_length=40)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def owners(self):
        return self.player_set.count()

    def get_icon_url(self):
        return f"http://media.steampowered.com/steamcommunity/public/images/apps/{self.appid}/{self.icon_id}.jpg"

    def get_logo_url(self):
        return f"http://media.steampowered.com/steamcommunity/public/images/apps/{self.appid}/{self.logo_id}.jpg"

    def __str__(self):
        return f"{self.name}"

    class Meta:
        ordering = ("name",)


class PlayerManager(models.Manager):
    def import_library(self, player):
        steam_app = SocialApp.objects.filter(provider="steam").first()
        api = WebAPI(key=steam_app.secret)

        games = api.IPlayerService.GetOwnedGames(
            steamid=player.steamid,
            include_appinfo=True,
            include_played_free_games=True,
            appids_filter=None,
        )["response"]

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
                print("Game %s created in DB" % game["name"])
            else:
                print("Game %s updated in DB" % game["name"])

            # User's stat on game
            GameStat.objects.update_or_create(
                player=player,
                game=game_obj,
                defaults={"playtime": game["playtime_forever"]},
            )


class Player(models.Model):
    objects = PlayerManager()
    steamid = models.BigIntegerField(primary_key=True)
    nickname = models.CharField(max_length=255)
    real_name = models.CharField(max_length=255)
    profile_url = models.URLField()

    avatar_url = models.URLField()
    avatar_m_url = models.URLField()
    avatar_f_url = models.URLField()

    games = models.ManyToManyField(Game, through="GameStat")

    country_code = models.CharField(max_length=4)

    creation_date = models.DateTimeField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nickname

    def get_currently_playing(self):
        return GameStat.objects.filter(player=self, status=PlayChoice.PLAYING)

    def get_finished(self):
        return GameStat.objects.filter(player=self, status=PlayChoice.FINISHED)

    class Meta:
        ordering = ("nickname",)


class GameStat(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    playtime = models.IntegerField(default=0)
    status = models.CharField(
        max_length=50,
        choices=[(state, state.value) for state in PlayChoice],
        default=PlayChoice.NONE,
    )

    started_at = models.DateTimeField(blank=True, null=True)
    finished_at = models.DateTimeField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def play(self):
        self.status = PlayChoice.PLAYING
        self.started_at = datetime.now()

        return self.save()

    def finish(self):
        self.status = PlayChoice.FINISHED
        self.finished_at = datetime.now()

        return self.save()


class Group(models.Model):
    group_id = models.BigIntegerField()
    name = models.CharField(max_length=255)
    headline = models.CharField(max_length=255, null=True)
    url = models.URLField()

    avatar_url = models.URLField()
    avatar_m_url = models.URLField()
    avatar_f_url = models.URLField()

    members = models.ManyToManyField(Player, related_name="groups")

    # Link to a Django site
    site = models.ForeignKey(Site, on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
