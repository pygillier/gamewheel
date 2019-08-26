from django.db import models


class Game(models.Model):
    appid = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=255)

    icon_id = models.CharField(max_length=40)
    logo_id = models.CharField(max_length=40)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def owners(self):
        return self.player_set.count()

    def get_icon_url(self):
        return f'http://media.steampowered.com/steamcommunity/public/images/apps/{self.appid}/{self.icon_id}.jpg'  # noqa

    def get_logo_url(self):
        return f'http://media.steampowered.com/steamcommunity/public/images/apps/{self.appid}/{self.logo_id}.jpg'  # noqa

    def __str__(self):
        return f"{self.name}"

    class Meta:
        ordering = ('name',)


class Player(models.Model):
    steamid = models.BigIntegerField(primary_key=True)
    nickname = models.CharField(max_length=255)
    real_name = models.CharField(max_length=255)
    profile_url = models.URLField()

    avatar_url = models.URLField()
    avatar_m_url = models.URLField()
    avatar_f_url = models.URLField()

    games = models.ManyToManyField(Game, through='GameStat')

    country_code = models.CharField(max_length=4)

    creation_date = models.DateTimeField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.nickname}"

    class Meta:
        ordering = ('nickname',)


class GameStat(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    playtime = models.IntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
