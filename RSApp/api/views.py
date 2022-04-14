import joblib
import pandas as pd
from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.
from rest_framework.decorators import api_view
from rest_framework.response import Response

from . import models
from .models import File
from .serializers import FileSerializer

from django.core.files.storage import FileSystemStorage
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel


def save_file(model, filename):
    joblib.dump(model, filename)


def load_file(filename):
    return joblib.load(filename)


@api_view(['GET'])
def apiOverview(request):
    api_urls = {
        'upload File': '/api/upload',
        'details':'api/detail/<id>',
        'files list': '/api/file_list',
        'get_recommendation': 'api/recom/<id>/<title>',
        'csv parameters': 'csv MUST HAVE fields overview and name'
    }
    return Response(api_urls)


@api_view(['GET'])
def FileList(request):
    files = File.objects.all()
    serializer = FileSerializer(files, many=True)
    return Response(serializer.data)


@api_view(['POST'])
def uploadFile(request):
    global result
    if request.method == "POST":
        # Fetching the form data
        fileTitle = request.POST["fileTitle"]
        uploadedFile = request.FILES["uploadedFile"]

        # Saving the information in the database
        document = models.File(
            title=fileTitle,
            uploadedFile=uploadedFile
        )
        document.save()
        try:
            metadata = pd.read_csv(document.uploadedFile, low_memory=False)

            tfidf = TfidfVectorizer(stop_words='english')

            metadata['overview'] = metadata['overview'].fillna('')

            tfidf_matrix = tfidf.fit_transform(metadata['overview'])

            cosine_sim = linear_kernel(tfidf_matrix, tfidf_matrix)

            save_file(cosine_sim, f'static/models/{document.id}.pkl')
        except:
            pass

        result = {
            'file id': document.id,
            'title': document.title,
            'file saved successes': True
        }

    return Response(result)


def upload_page(request):
    context = {}
    return render(request, 'api/upload.html', context)


@api_view(['GET'])
def get_recommendation(request, id, title):
    try:
        file = File.objects.get(id=id)

        metadata = pd.read_csv(file.uploadedFile.path, low_memory=False)

        indices = metadata['title'].drop_duplicates().reset_index().set_index('title')['index']

        idx = indices[title]

        sim_scores = list(enumerate(load_file(f'static/models/{id}.pkl')[idx]))

        sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

        sim_scores = sim_scores[1:11]

        movie_indices = [i[0] for i in sim_scores]

        recommendation = metadata['title'].iloc[movie_indices]
    except:
        recommendation = {'error': 'bad file'}

    return Response(recommendation)


@api_view(['GET'])
def get_details(request, id):

    file = File.objects.get(id=id)

    metadata = open(file.uploadedFile.path,'r')

    return Response(metadata)
