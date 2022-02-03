from django.shortcuts import render
from .recommendsManager import Manager


# Create your views here.
def index(request):
    context = {}
    return render(request, 'RecSys/index.html', context)


def recommend_film(request):
    film_name = request.POST['content_name']
    manager = Manager()

    context = {'recommendations': manager.get_recommendations(film_name)}

    return render(request, 'RecSys/index.html', context)
