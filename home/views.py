from django.views.generic import TemplateView


class HomeView(TemplateView):
    template_name = 'home/home.html'


class PlayView(TemplateView):
    template_name = 'home/play.html'
