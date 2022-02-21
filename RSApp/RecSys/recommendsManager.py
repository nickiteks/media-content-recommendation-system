import joblib
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
import requests


class Manager:

    def __init__(self,data):
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
        url = "https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US".format(
            movie_id)
        data = requests.get(url)
        data = data.json()
        try:
            poster_path = data['poster_path']
        except:
            poster_path = ''
        full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
        return full_path

    # Возвраем список рекомендаций и постеры
    def get_recommendations_film(self, title):
        idx = self.indices[title]

        sim_scores = list(enumerate(self.cosine_sim[idx]))

        sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

        sim_scores = sim_scores[1:11]

        movie_indices = [i[0] for i in sim_scores]

        recommended_movie_posters = []
        print(f'indexes{movie_indices}\n')
        for i in movie_indices:
            recommended_movie_posters.append(self.fetch_poster_film(self.metadata['id'][i]))

        return self.metadata['title'].iloc[movie_indices], recommended_movie_posters

    def fetch_poster_series(self, series_id):
        url = "https://api.themoviedb.org/3/tv/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US".format(
            series_id)
        data = requests.get(url)
        data = data.json()
        try:
            poster_path = data['poster_path']
        except:
            poster_path = ''
        full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
        return full_path

    def get_recommendations_series(self, title):
        idx = self.indices[title]

        sim_scores = list(enumerate(self.cosine_sim[idx]))

        sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

        sim_scores = sim_scores[1:11]

        movie_indices = [i[0] for i in sim_scores]

        recommended_movie_posters = []
        print(f'indexes{movie_indices}\n')
        for i in movie_indices:
            recommended_movie_posters.append(self.fetch_poster_series(self.metadata['id'][i]))

        return self.metadata['title'].iloc[movie_indices], recommended_movie_posters

class Recommendation:
    def __init__(self, title, path):
        self.title = title
        self.poster_path = path
