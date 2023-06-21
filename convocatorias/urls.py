from django.urls import path
from .views import index, download_pdf

app_name = 'convocatorias'

urlpatterns = [
    path('download-pdf/', download_pdf, name='download_pdf'),
]
