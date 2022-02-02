from django.shortcuts import render


# Create your views here.
def index(request):
    context = {}
    return render(request, 'RecSys/index.html', context)


def recommend_film(request):
    context = {}
    print(request.POST['content_name'])
    return render(request, 'RecSys/index.html', context)
