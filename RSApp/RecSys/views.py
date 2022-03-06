from django.shortcuts import render
from .recommendsManager import Manager, Recommendation
from . import config

# Create your views here.
def index(request):
    context = {}
    return render(request, 'RecSys/index.html', context)


def recommend_series(request):
    series_name = request.POST['content_name_series']
    manager = Manager()
    manager.prepare_movie_series_recommendation(config.FILE_SERIES)

    recommendations, posters = manager.get_recommendations_series(series_name)

    recommendations_list = []
    posters_list = []

    for i in recommendations:
        recommendations_list.append(i)

    result = []
    for i in range(len(recommendations_list)):
        result.append(Recommendation(recommendations_list[i], posters[i]))

    context = {'recommendations': result}

    return render(request, 'RecSys/index.html', context)


def recommend_film(request):
    film_name = request.POST['content_name_film']
    manager = Manager()
    manager.prepare_movie_series_recommendation(config.FILE_FILM)

    recommendations, posters = manager.get_recommendations_film(film_name)

    recommendations_list = []
    posters_list = []

    for i in recommendations:
        recommendations_list.append(i)

    result = []
    for i in range(len(recommendations_list)):
        result.append(Recommendation(recommendations_list[i], posters[i]))

    context = {'recommendations': result}

    return render(request, 'RecSys/index.html', context)


def recommend_game(request):
    pass


def film_page(request):
    context = {}
    return render(request, 'RecSys/film.html', context)


def series_page(request):
    context = {}
    return render(request, 'RecSys/series.html', context)


def game_page(request):
    context = {}
    return render(request, 'RecSys/game.html', context)
