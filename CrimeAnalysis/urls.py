from django.urls import path
from  CrimeAnalysis.views import CrimeAnalysis


urlpatterns = [
    path('crime-analysis/', CrimeAnalysis.as_view(), name='crimeanalysis'),
]
