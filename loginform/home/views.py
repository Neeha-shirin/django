from django.db import models
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as auth_login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.cache import never_cache,cache_control
from .forms import Aforms
from .models import Amodel
from django.db.models import Q

@never_cache
def index(request):
    return render(request, 'index.html')

@never_cache
def signup(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        confirmpassword = request.POST['confirmpassword']
        
        if password == confirmpassword:
            if User.objects.filter(username=username).exists():
                messages.info(request, 'Username already exists')
                return redirect('signup')
            else:
                User.objects.create_user(username=username, password=password)
                messages.info(request, 'User created successfully')
                return redirect('login')
        else:
            messages.error(request, 'Passwords do not match')
            return redirect('signup')
    return render(request, 'signup.html')

@never_cache
def login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            auth_login(request, user)
            if user.is_staff:  
                return redirect('adduser')  
            else:
                return redirect('homepage')  
        else:
            return render(request, 'login.html', {'error': 'Incorrect username or password'})
    return render(request, 'login.html')

@login_required(login_url='login')
@never_cache
@cache_control(no_cache=True,must_revalidate=True,no_store=True)
def homepage(request):
    username = request.user.username
    return render(request, 'homepage.html', {'username': username})

@cache_control(no_cache=True,must_revalidate=True,no_store=True)
def logout_view(request):
    logout(request)
    return redirect('login')

@login_required(login_url='login')
@never_cache
@cache_control(no_cache=True,must_revalidate=True,no_store=True)
def adduser(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        
        if name and email:
            user = Amodel(name=name, email=email)
            user.save()
            messages.success(request, 'User added successfully')
            return redirect('adduser')
        else:
            messages.error(request, 'Both fields are required.')

    search_query = request.GET.get('search', '')
    if search_query:
        users = Amodel.objects.filter(Q(name__icontains=search_query) | Q(email__icontains=search_query))
    else:
        users = Amodel.objects.all()
    
    return render(request, 'adduser.html', {'users': users, 'search_query': search_query})

@cache_control(no_cache=True,must_revalidate=True,no_store=True)
def deleteuser(request, user_id):
    user = get_object_or_404(Amodel, pk=user_id)
    user.delete()
    messages.success(request, 'User deleted successfully')
    return redirect('adduser')

@cache_control(no_cache=True,must_revalidate=True,no_store=True)
def updateuser(request, user_id):
    user = get_object_or_404(Amodel, pk=user_id)
    
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        
        if name and email: 
            user.name = name
            user.email = email
            user.save()
            messages.success(request, 'User updated successfully')
            return redirect('adduser')
        else:
            messages.error(request, 'Both fields are required.')
    
    return render(request, 'updateuser.html', {'user': user})
