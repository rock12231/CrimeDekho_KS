from django.urls import path
from Test.views import Test


urlpatterns = [ 
        path('test/', Test.as_view(), name='test'),
]
