from django.views import View
from CrimeMapping import views
from django.shortcuts import render
from CrimeMapping.views import cards


class About(View):
    def get(self, request):
        views.cardData()
        return render(request, 'About/about.html',{"cards":cards})
    
    def post(self, request):
        pass
  

class Contact(View):
    def get(self, request):
        return render(request, 'About/contact.html')
    