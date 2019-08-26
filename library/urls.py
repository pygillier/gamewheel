from django.urls import path
from library  import views

app_name = 'library'
urlpatterns = [
    path('profile/', views.MyProfileView.as_view(), name='my_profile'),
    path('games/', views.ByPlayerView.as_view(), name='my_library'),
    path('import/', views.ImportLibraryView.as_view(), name='import_library'),
    path('play/<int:appid>', views.MarkAsPlayingView.as_view(), name='mark_play'),
]