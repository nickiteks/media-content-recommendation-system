from django.shortcuts import render, redirect
from .recommendsManager import Manager, Recommendation
from . import config
from .forms import CreateUserForm
from .models import *
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout


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
    film_name = request.POST['content_name_game']
    manager = Manager()
    manager.prepare_game_recomendation(config.FILE_GAME)

    recommendations, posters = manager.get_recomendation_game(film_name)

    recommendations_list = []
    posters_list = []

    for i in recommendations:
        recommendations_list.append(i)

    result = []
    for i in range(len(recommendations_list)):
        result.append(Recommendation(recommendations_list[i], posters[i]))

    context = {'recommendations': result}

    return render(request, 'RecSys/index.html', context)


def film_page(request):
    context = {}
    return render(request, 'RecSys/film.html', context)


def series_page(request):
    context = {}
    return render(request, 'RecSys/series.html', context)


def game_page(request):
    context = {}
    return render(request, 'RecSys/game.html', context)


def registerPage(request):
    form = CreateUserForm()

    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()

            user = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            u = User.objects.get(username=user)
            messages.success(request, 'Account was created for ' + user)

            customer, created = Customer.objects.get_or_create(
                email=email,
                user=u,
                name=user
            )
            customer.save()

            return redirect('login')

    context = {'form': form}
    return render(request, "RecSys/register.html", context)


def loginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            messages.info(request, 'incorrect')

    context = {}
    return render(request, "RecSys/login.html", context)


def logoutUser(request):
    logout(request)
    return redirect('login')
