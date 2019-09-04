from django.urls import path
from home import views

app_name = 'home'
urlpatterns = [
    path('', views.HomeView.as_view(), name='index'),
    path('play/', views.PlayView.as_view(), name='play')
]