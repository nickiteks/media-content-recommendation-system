from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.apiOverview, name='api_overview'),
    path('file_list/', views.FileList, name='file_list'),
    path('upload/', views.upload_page, name='upload'),
    path('upload_file/', views.uploadFile, name='upload_file'),
    path('recom/<int:id>/<str:title>', views.get_recommendation, name='recom')
]

urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
