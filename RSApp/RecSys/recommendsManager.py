import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel


class Manager:
    def __init__(self):
        # Данные фильмов
        self.metadata = pd.read_csv('C:\\Users\\NULS\\PycharmProjects\\media-content-recommendation-system\\RSApp\\RecSys\\movies_metadata.csv', low_memory=False)

        tfidf = TfidfVectorizer(stop_words='english')

        self.metadata['overview'] = self.metadata['overview'].fillna('')

        tfidf_matrix = tfidf.fit_transform(self.metadata['overview'])
        self.cosine_sim = linear_kernel(tfidf_matrix, tfidf_matrix)

        self.indices = pd.Series(self.metadata.index, index=self.metadata['title']).drop_duplicates()

    def get_recommendations(self, title):
        idx = self.indices[title]

        sim_scores = list(enumerate(self.cosine_sim[idx]))

        sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

        sim_scores = sim_scores[1:11]

        movie_indices = [i[0] for i in sim_scores]

        return self.metadata['title'].iloc[movie_indices]