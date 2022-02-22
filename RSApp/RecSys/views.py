from django.shortcuts import render
from .recommendsManager import Manager, Recommendation


# Create your views here.
def index(request):
    context = {}
    return render(request, 'RecSys/index.html', context)


def recommend_series(request):
    series_name = request.POST['content_name_series']
    manager = Manager()
    manager.prepare_movie_series_recommendation('/Users/nikita/PycharmProjects/media-content-recommendation-system'
                                                '/RSApp/static/data/series_dataset.csv')

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
    manager.prepare_movie_series_recommendation('/Users/nikita/PycharmProjects/media-content-recommendation-system'
                                                '/RSApp/static/data/tmdb_5000_movies.csv')

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