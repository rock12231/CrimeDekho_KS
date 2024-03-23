from django.urls import path
from  CrimeAnalysis.views import CrimeAnalysis, CrimeAnalysisChart, CrimeAnalysisTable


urlpatterns = [
    path('crime-analysis/', CrimeAnalysis.as_view(), name='crimeanalysis'),
    path('crime-analysis/chart/', CrimeAnalysisChart.as_view(), name='crimeanalysischart'),
    path('crime-analysis/table/', CrimeAnalysisTable.as_view(), name='crimeanalysistable'),
]
