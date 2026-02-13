
from django.shortcuts import render, redirect
import pandas as pd
from .forms import RegisterForm
from django.contrib.auth import authenticate, login, logout
from .models import Movie, CustomUser
import random
from django.db.models import Q
from django.shortcuts import get_object_or_404
from .utils import recommendation
import ast
from django.core.paginator import Paginator
import pycountry
from django.contrib.auth.decorators import login_required
# Create your views here.
def movies(request):
    popular_movies = Movie.objects.all().order_by('-popularity')[:20]
    all_movies = list(Movie.objects.all())
    random_movies = random.sample(all_movies, 30)  

    return render(request, 'home/home.html',{'populars': popular_movies, 'all_movies': all_movies, 'randoms': random_movies})

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            print(form.cleaned_data)
            form.save()
            return redirect('login')
        else:
            print(form.errors)
    else:
        form = RegisterForm()   
    return render(request, 'home/registration.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        user = authenticate(request, 
            username=request.POST['username'], 
            password=request.POST['password']
        )
        if user is not None:
            login(request, user)
            return redirect('movies')
        else:
            return render(request, 'home/login.html', {'error': 'Invalid username or password'})
        
    return render(request, 'home/login.html')
        

def user_logout(request):
    logout(request)
    return redirect('movies')


def search_movies(request):
    
    query = request.GET.get('query')


    if query:
        movie = Movie.objects.filter( title__icontains=query
        ).first()

        if movie:
            return redirect('movie_detail', id=movie.id)
        
    return redirect('movies')


def movie_detail(request, id):
    movie = get_object_or_404(Movie, id=id)
    recommended_movies = recommendation(id)

    return render(request, 'home/movie_detail.html', {'searched_movie': movie, 'recommended_movies': recommended_movies})


def profile(request, id):
    user = get_object_or_404(CustomUser,id=id)
    return render(request, 'home/profile.html', {'user': user})

def get_movies_by_genres(request, genres):
    movies = Movie.objects.filter(genres__icontains = genres).order_by('-popularity')

    paginator = Paginator(movies, 30)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'movies' : page_obj,
        'page_obj': page_obj,
        'title' : f"{genres} movies"
    }

    return render(request, 'home/movies_genres.html', context)

def get_movies_by_langs(request, spoken_languages):
    movies = Movie.objects.filter(spoken_languages__icontains = spoken_languages).order_by('-popularity')

    paginator = Paginator(movies, 30)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    title_language = pycountry.languages.get(alpha_2 = spoken_languages)
    title = title_language.name

    context = {
        'movies' : page_obj,
        'page_obj' : page_obj,
        'title' : f"{title} movies" ,
    }

    return render(request, 'home/movies_languages.html', context)


@login_required(login_url='login')
def download(request):
    return render(request, 'home/download.html')