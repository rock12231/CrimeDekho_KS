from django.urls import path
from  Account.views import Login, Register, Logout, Profile


urlpatterns = [
    path('login/', Login.as_view(), name='login'),
    path('logout/', Logout.as_view(), name='logout'),
    path('profile/', Profile.as_view(), name='profile'),
    path('register/', Register.as_view(), name='register'),
]
