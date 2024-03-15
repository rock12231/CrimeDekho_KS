from django.views import View
from django.contrib import messages
from django.contrib.auth.models import User
from django.shortcuts import render, redirect 
from django.contrib.auth import authenticate, login, logout


class Login(View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('/')
        return render(request, 'Account/login.html')
        
    def post(self, request):
        if request.method == 'POST':
            user = authenticate(request, username=request.POST['username'], password=request.POST['password'], is_staff=True)
            if user is not None:
                login(request, user)
                messages.success(request, 'You have successfully logged in as ' + request.POST['username'] + '')
                if user.is_superuser :
                    return redirect('profile')
                return redirect('/') 
            else:
                messages.error(request, 'Username or password does not exist')
                return redirect('login')
        return render(request, 'Account/login.html')


class Register(View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('/')
        return render(request, 'Account/register.html')
    
    def post(self, request):
        if request.method=='POST':
            fullname = request.POST['fullname'].split()
            first_name = fullname[0]
            last_name = fullname[1] if len(fullname) > 1 else ""
            if len(request.POST['username']) >= 4 or len(request.POST['password']) >= 4:
                user = User.objects.create_user(username=request.POST['username'], email=request.POST['email'],password=request.POST['password'], first_name=first_name, last_name=last_name)
                user.save()
                login(request, user)
                messages.success(request, 'You have successfully registered as ' + request.POST['username'] + ' Compete your profile')
                return redirect('/')
            else:
                messages.error(request, 'Username or password must be grater than 4')
                return redirect('register')
        else:
            messages.error(request, 'Invalid input')
            return redirect('register')


class Profile(View):
    def get(self, request):
        if request.user.is_authenticated:
            if request.user.is_superuser and request.user.is_staff:
                userslist= User.objects.filter(is_superuser=False).values( 'id', 'username', 'first_name', 'last_name', 'email', 'is_active', 'is_staff', 'last_login')
                context = {'users': userslist}
            if not request.user.is_superuser and request.user.is_active:
                user = User.objects.get(username=request.user.username)
                context = {'user': user}
            return render(request, 'Account/profile.html', context)
        else:
            messages.error(request, 'Invalid input')
            return redirect('login')
    
    def post(self, request):
        id = request.POST.get('user_id', None)
        if id is not None:
            if request.user.is_authenticated and request.user.is_superuser:
                user = User.objects.get(pk=id)
                user.is_active = request.POST.get('active') == 'on'
                user.is_staff =request.POST.get('staff') == 'on'
                user.save()
                messages.success(request, 'You have successfully updated user profile')
                return redirect('profile')
            else:
                messages.error(request, 'Invalid input')
                return redirect('profile')
        if request.method=='POST' :
            if request.user.is_authenticated and request.user.is_superuser:
                userslist= User.objects.filter(is_superuser=False).values( 'id', 'username', 'first_name', 'last_name', 'email', 'is_active', 'is_staff', 'last_login')
                context = {'users': userslist}
                messages.success(request, 'You have successfully updated user profile')
            if request.user.is_authenticated:
                user = User.objects.get(username=request.user.username)
                user.first_name = request.POST['first_name']
                user.last_name = request.POST['last_name']
                user.save()
                user = User.objects.get(username=request.user.username)
                context = {'user': user}
                messages.success(request, 'You have successfully updated your profile')
            return render(request, 'Account/profile.html', context)
        else:
            messages.error(request, 'Invalid input')
        return render(request, '/')
    

class Logout(View):
    def get(self, request):    
        logout(request)
        return redirect('/')