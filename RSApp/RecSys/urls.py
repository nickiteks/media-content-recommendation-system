from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('/recommend_film', views.recommend_film, name='recommend')
]
