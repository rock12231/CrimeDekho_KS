from CrimeAPI import views
from django.urls import path


urlpatterns = [
    path('api/crime/', views.CrimeAPI.as_view()),
]
