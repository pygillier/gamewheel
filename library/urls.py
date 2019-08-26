from django.urls import path
from library  import views

app_name = 'library'
urlpatterns = [
    path('profile/', views.MyProfileView.as_view(), name='my_profile'),
    path('games/', views.ByPlayerView.as_view(), name='my_library'),
]