import os
import secrets
import shutil

import joblib
import pandas as pd
from django.shortcuts import render, redirect
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel

from .recommendsManager import Manager, Recommendation
from . import config
from .forms import CreateUserForm
from .models import *
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .config import FILE_FILM, FILE_GAME, FILE_SERIES


def index(request):
    context = {}
    return render(request, 'RecSys/main.html', context)


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
    metadata = pd.read_csv(FILE_SERIES, low_memory=False)
    series = metadata['title']
    context = {"Series": series}
    return render(request, 'RecSys/series.html', context)


def game_page(request):
    metadata = pd.read_csv(FILE_GAME, low_memory=False)
    games = metadata['Name']
    context = {'Games': games}
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

            access_token = token.objects.create(
                customer=customer,
                generated_token=secrets.token_hex()
            )
            access_token.save()

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
    media = None
    if request.user.is_authenticated:
        customer = request.user.customer
        media_adding(title, 'film', customer)
        media = mediaContent.objects.filter(customer=customer)

    context = {"medias": media}
    return render(request, 'RecSys/media.html', context)


def add_media_series(request, title):
    media = None
    if request.user.is_authenticated:
        customer = request.user.customer
        media_adding(title, 'series', customer)
        media = mediaContent.objects.filter(customer=customer)

    context = {"medias": media}
    return render(request, 'RecSys/media.html', context)


def add_media_game(request, title):
    media = None
    if request.user.is_authenticated:
        customer = request.user.customer
        media_adding(title, 'game', customer)
        media = mediaContent.objects.filter(customer=customer)

    context = {"medias": media}
    return render(request, 'RecSys/media.html', context)


def media_adding(title, category, customer):
    media, created = mediaContent.objects.get_or_create(title=title, category=category, customer=customer)
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


def user_data_page(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        user_data = userData.objects.filter(customer=customer)

        context = {"userData": user_data}
        return render(request, 'RecSys/userData.html', context)


def save_file(model, filename):
    joblib.dump(model, filename)


def load_file(filename):
    return joblib.load(filename)


def upload_user_file(request):
    if request.user.is_authenticated:
        try:
            if request.method == "POST":

                document = userData(
                    title=request.POST["fileTitle"],
                    uploadedFile=request.FILES["uploadedFile"],
                    customer=request.user.customer
                )
                document.save()

                try:
                    metadata = pd.read_csv(document.uploadedFile, low_memory=False)

                    tfidf = TfidfVectorizer(stop_words='english')

                    metadata['overview'] = metadata['overview'].fillna('')

                    tfidf_matrix = tfidf.fit_transform(metadata['overview'])

                    cosine_sim = linear_kernel(tfidf_matrix, tfidf_matrix)

                    save_file(cosine_sim, f'static/modelsUser/{document.id}.pkl')

                    metadata.close()
                    f = open(request.FILES["uploadedFile"], 'wb+')
                    f.close()

                except:
                    pass
        except:
            pass

        return redirect('user_data')


def user_data_recom_page(request, id):
    file = userData.objects.get(id=id)
    metadata = pd.read_csv(file.uploadedFile.path, low_memory=False)

    context = {'UserData': metadata['title'], 'file_id': id}
    return render(request, 'RecSys/userDataRecom.html', context)


def recommend_user_data(request, id):
    if request.user.is_authenticated:
        try:
            title = request.POST['content_name_user_data']

            file = userData.objects.get(id=id)

            metadata = pd.read_csv(file.uploadedFile.path, low_memory=False)

            indices = metadata['title'].drop_duplicates().reset_index().set_index('title')['index']

            idx = indices[title]

            sim_scores = list(enumerate(load_file(f'static/modelsUser/{id}.pkl')[idx]))

            sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

            sim_scores = sim_scores[1:11]

            movie_indices = [i[0] for i in sim_scores]

            recommendation = metadata['title'].iloc[movie_indices]
        except:
            recommendation = []

        context = {'recommendations': recommendation}
        return render(request, 'RecSys/userData_recomendation.html', context)


def delete_user_file(request, id):
    if request.user.is_authenticated:
        data = userData.objects.get(id=id)
        os.remove(f'static/modelsUser/{id}.pkl')
        data.delete()

    return redirect('user_data')
