from django.urls import path
from  FIR.views import Addcrime, Policestations, FIR

urlpatterns = [
    path('add-crime/', Addcrime.as_view(), name='addcrime'),
    path('police-stations/', Policestations.as_view(), name='policestations'),
    path('fir/', FIR.as_view(), name='fir')
]
