from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('recommend_film/', views.recommend_film, name='recommend_film'),
    path('recommend_series/', views.recommend_series, name='recommend_series'),
    path('recommend_game/', views.recommend_game, name='recommend_game'),
    path('film_page/', views.film_page, name='film_page'),
    path('game_page/', views.game_page, name='game_page'),
    path('series_page/', views.series_page, name='series_page'),
    path('register/', views.registerPage, name='register'),
    path('login/', views.loginPage, name='login'),
    path('<str:title>/add_media_film/', views.add_media_film, name='add_media_film'),
    path('<str:title>/add_media_game/', views.add_media_game, name='add_media_game'),
    path('<str:title>/add_media_series/', views.add_media_series, name='add_media_series'),
    path('media_page/', views.media_page, name='media_page'),
    path('<int:media_id>/delete_from_media/', views.delete_from_media,name='delete_from_media')
]
