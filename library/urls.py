from django.urls import path
from library  import views

app_name = 'library'
urlpatterns = [
    path('', views.ByPlayerView.as_view(), name='my_library'),
    path('profile/', views.MyProfileView.as_view(), name='my_profile'),
    path('import/', views.ImportLibraryView.as_view(), name='import_library'),
    path('<int:appid>/playing', views.MarkAsPlayingView.as_view(), name='mark_play'),
    path('<int:appid>/finished', views.MarkAsFinishedView.as_view(), name='mark_finished'),
]