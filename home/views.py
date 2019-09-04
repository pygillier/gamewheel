from django.views.generic import TemplateView

from library.models import Game


class HomeView(TemplateView):
    template_name = "home/home.html"


class PlayView(TemplateView):
    template_name = "home/play.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["game"] = (
            Game.objects.filter(
                player=self.request.user.get_player(), gamestat__status="unknown"
            )
            .random()
            .first()
        )

        return context
