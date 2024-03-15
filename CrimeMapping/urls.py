from django.urls import path
from  CrimeMapping.views import Crimemapping


urlpatterns = [ 
                path('crime-mapping/', Crimemapping.as_view(), name='crimemapping'),
        ]
