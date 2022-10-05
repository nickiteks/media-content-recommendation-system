import os
from django.templatetags.static import static

FILE_FILM = os.path.join(os.path.dirname(os.path.dirname(__file__)),'static//data//tmdb_5000_movies.csv')
FILE_SERIES = os.path.join(os.path.dirname(os.path.dirname(__file__)),'static//data//series_dataset.csv')


FILE_GAME= os.path.join(os.path.dirname(os.path.dirname(__file__)),'static//data//games.csv')
API_KEY ='8265bd1679663a7ea12ac168da84d2e8'
RAWG='7c70e86869c7461f95fb64762ed01acf'