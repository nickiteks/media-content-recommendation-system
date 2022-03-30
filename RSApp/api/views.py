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


def load_file(self, filename):
    return joblib.load(filename)


@api_view(['GET'])
def apiOverview(request):
    api_urls = {
        'upload File': '/api/upload'
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

        metadata = pd.read_csv(document.uploadedFile, low_memory=False)

        tfidf = TfidfVectorizer(stop_words='english')

        metadata['overview'] = metadata['overview'].fillna('')

        tfidf_matrix = tfidf.fit_transform(metadata['overview'])

        cosine_sim = linear_kernel(tfidf_matrix, tfidf_matrix)

        save_file(cosine_sim, f'static/models/{document.id}.pkl')

        result = {
            'file id': document.id,
            'file saved successes': True
        }

    return Response(result)


def upload_page(request):
    context = {}
    return render(request, 'api/upload.html', context)
