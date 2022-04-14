import pandas as pd
from django.shortcuts import render, redirect
from .recommendsManager import Manager, Recommendation
from . import config
from .forms import CreateUserForm
from .models import *
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .config import FILE_FILM
from django.urls import reverse


def index(request):
    context = {}
    return render(request, 'RecSys/index.html', context)


def recommend_series(request):
    series_name = request.POST['content_name_series']
    media = []

    if request.user.is_authenticated:
        customer = request.user.customer
        media = mediaContent.objects.filter(customer=customer, category='series')

    manager = Manager()
    manager.prepare_movie_series_recommendation(config.FILE_SERIES)

    recommendations, posters = manager.get_recommendations_series(series_name, media)

    recommendations_list = []
    posters_list = []

    for i in recommendations:
        recommendations_list.append(i)

    result = []
    for i in range(len(recommendations_list)):
        result.append(Recommendation(recommendations_list[i], posters[i]))

    context = {'recommendations': result}

    return render(request, 'RecSys/series_recomendation.html', context)


def recommend_film(request):
    film_name = request.POST['content_name_film']
    media = []

    if request.user.is_authenticated:
        customer = request.user.customer
        media = mediaContent.objects.filter(customer=customer, category='film')

    manager = Manager()
    manager.prepare_movie_series_recommendation(config.FILE_FILM)

    recommendations, posters = manager.get_recommendations_film(film_name, media)

    recommendations_list = []
    posters_list = []

    for i in recommendations:
        recommendations_list.append(i)

    result = []
    for i in range(len(recommendations_list)):
        result.append(Recommendation(recommendations_list[i], posters[i]))

    context = {'recommendations': result}

    return render(request, 'RecSys/film_recomendation.html', context)


def recommend_game(request):
    film_name = request.POST['content_name_game']

    media = []

    if request.user.is_authenticated:
        customer = request.user.customer
        media = mediaContent.objects.filter(customer=customer, category='game')

    manager = Manager()
    manager.prepare_game_recomendation(config.FILE_GAME)

    recommendations, posters = manager.get_recomendation_game(film_name, media)

    recommendations_list = []
    posters_list = []

    for i in recommendations:
        recommendations_list.append(i)

    result = []
    for i in range(len(recommendations_list)):
        result.append(Recommendation(recommendations_list[i], posters[i]))

    context = {'recommendations': result}

    return render(request, 'RecSys/game_recomendation.html', context)


def film_page(request):
    metadata = pd.read_csv(FILE_FILM, low_memory=False)
    films = metadata['title']
    context = {'Films': films}
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


def add_media_film(request, title):
    if request.user.is_authenticated:
        customer = request.user.customer
        media_adding(title, 'film', customer)

    context = {}
    return render(request, 'RecSys/index.html', context)


def add_media_series(request, title):
    if request.user.is_authenticated:
        customer = request.user.customer
        media_adding(title, 'series', customer)

    context = {}
    return render(request, 'RecSys/index.html', context)


def add_media_game(request, title):
    if request.user.is_authenticated:
        customer = request.user.customer
        media_adding(title, 'game', customer)

    context = {}
    return render(request, 'RecSys/index.html', context)


def media_adding(title, category, customer):
    media = mediaContent.objects.create(title=title, category=category, customer=customer)
    media.save()


def media_page(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        media = mediaContent.objects.filter(customer=customer)

        context = {"medias": media}
        return render(request, 'RecSys/media.html', context)


def delete_from_media(request, media_id):
    if request.user.is_authenticated:
        try:
            media = mediaContent.objects.get(id=media_id)
        except:
            media = None
        media.delete()
        return redirect('media_page')


def search_media(request):
    if request.user.is_authenticated:
        search = request.POST['search_media']
        customer = request.user.customer

        media = mediaContent.objects.filter(title__icontains=search, customer=customer)

        context = {"medias": media}
        return render(request, 'RecSys/media.html', context)


def get_media_films(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        media = mediaContent.objects.filter(customer=customer, category='film')

        context = {"medias": media}
        return render(request, 'RecSys/media.html', context)


def get_media_series(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        media = mediaContent.objects.filter(customer=customer, category='series')

        context = {"medias": media}
        return render(request, 'RecSys/media.html', context)


def get_media_games(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        media = mediaContent.objects.filter(customer=customer, category='game')

        context = {"medias": media}
        return render(request, 'RecSys/media.html', context)
