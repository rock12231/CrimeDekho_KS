from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static

urlpatterns = [
    # Admin URL
    path('admin/', admin.site.urls),
    # App's URL
    path('', include('FIR.urls')),
    path('', include('Home.urls')),
    path('', include('Test.urls')),
    path('', include('About.urls')),
    path('', include('Account.urls')),
    path('', include('CrimeAPI.urls')),
    path('', include('CrimeMapping.urls')),
    path('', include('CrimeAnalysis.urls')),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
