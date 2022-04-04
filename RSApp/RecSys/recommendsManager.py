import joblib
import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
import requests
from bs4 import BeautifulSoup
from .config import API_KEY


class Manager:

    def prepare_movie_series_recommendation(self, data):
        # Данные фильмов
        self.metadata = pd.read_csv(
            data,
            low_memory=False)

        tfidf = TfidfVectorizer(stop_words='english')

        self.metadata['overview'] = self.metadata['overview'].fillna('')

        tfidf_matrix = tfidf.fit_transform(self.metadata['overview'])

        self.cosine_sim = linear_kernel(tfidf_matrix, tfidf_matrix)

        self.indices = self.metadata['title'].drop_duplicates().reset_index().set_index('title')['index']

    def save_file(self, model, filename):
        joblib.dump(model, filename)

    def load_file(self, filename):
        return joblib.load(filename)

    def fetch_poster_film(self, movie_id):
        url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={API_KEY}&language=en-US"
        data = requests.get(url)
        data = data.json()
        try:
            poster_path = data['poster_path']
        except:
            poster_path = ''
        full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
        return full_path

    # Возвраем список рекомендаций и постеры
    def get_recommendations_film(self, title, media):
        media_indexes = []

        for i in media:
            media_indexes.append(self.metadata.index[self.metadata['title'] == i.title].tolist())

        idx = self.indices[title]

        sim_scores = list(enumerate(self.cosine_sim[idx]))

        sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

        sim_result = []
        count = 11
        i = 1
        while i < count:
            trigger = True
            for j in media_indexes:
                if sim_scores[i][0] == j[0]:
                    trigger = False
                    count += 1
            if trigger:
                sim_result.append(sim_scores[i])
            i += 1

        movie_indices = [i[0] for i in sim_result]

        recommended_movie_posters = []
        for i in movie_indices:
            recommended_movie_posters.append(self.fetch_poster_film(self.metadata['id'][i]))

        return self.metadata['title'].iloc[movie_indices], recommended_movie_posters

    def fetch_poster_series(self, series_id):
        url = f"https://api.themoviedb.org/3/tv/{series_id}?api_key={API_KEY}&language=en-US"
        data = requests.get(url)
        data = data.json()
        try:
            poster_path = data['poster_path']
        except:
            poster_path = ''
        full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
        return full_path

    def get_recommendations_series(self, title, media):
        media_indexes = []

        for i in media:
            media_indexes.append(self.metadata.index[self.metadata['title'] == i.title].tolist())

        idx = self.indices[title]

        sim_scores = list(enumerate(self.cosine_sim[idx]))

        sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

        sim_result = []
        count = 11
        i = 1
        while i < count:
            trigger = True
            for j in media_indexes:
                if sim_scores[i][0] == j[0]:
                    trigger = False
                    count += 1
            if trigger:
                sim_result.append(sim_scores[i])
            i += 1

        movie_indices = [i[0] for i in sim_result]

        recommended_movie_posters = []
        for i in movie_indices:
            recommended_movie_posters.append(self.fetch_poster_series(self.metadata['id'][i]))

        return self.metadata['title'].iloc[movie_indices], recommended_movie_posters

    def prepare_game_recomendation(self, data):
        self.metadata = pd.read_csv(data, low_memory=False)

        tfidf = TfidfVectorizer(stop_words='english')

        self.metadata['description'] = self.metadata['description'].fillna('')

        tfidf_matrix = tfidf.fit_transform(self.metadata['description'])

        self.cosine_sim = linear_kernel(tfidf_matrix, tfidf_matrix)

        self.indices = self.metadata['Name'].drop_duplicates().reset_index().set_index('Name')['index']

    def get_recomendation_game(self, title, media):
        media_indexes = []

        for i in media:
            media_indexes.append(self.metadata.index[self.metadata['Name'] == i.title].tolist())

        idx = self.indices[title]

        sim_scores = list(enumerate(self.cosine_sim[idx]))

        sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

        sim_result = []
        count = 11
        i = 1
        while i < count:
            trigger = True
            for j in media_indexes:
                if sim_scores[i][0] == j[0]:
                    trigger = False
                    count += 1
            if trigger:
                sim_result.append(sim_scores[i])
            i += 1

        movie_indices = [i[0] for i in sim_result]

        recommended_movie_posters = []
        for i in movie_indices:
            recommended_movie_posters.append(self.metadata['background_image'][i])
        return self.metadata['Name'].iloc[movie_indices], recommended_movie_posters

    def delete_from_metadata(self, media):
        for i in media:
            try:
                self.metadata = self.metadata.loc[self.metadata['title'] == i.title]
            except:
                pass


class Recommendation:
    def __init__(self, title, path):
        self.title = title
        self.poster_path = path
