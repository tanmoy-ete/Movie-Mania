
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
    # Get popular movies (this line is fine)
    popular_movies = Movie.objects.all().order_by('-popularity')[:20]

    # Get all movies safely
    all_movies_qs = Movie.objects.all()
    all_movies = list(all_movies_qs)

    # Debug print – very useful on Render logs
    print(f"DEBUG: Number of movies in Render DB = {len(all_movies)}")

    # Safe random selection – never crash
    desired_count = 30
    if len(all_movies) == 0:
        random_movies = []
    else:
        sample_size = min(len(all_movies), desired_count)
        random_movies = random.sample(all_movies, sample_size)

    context = {
        'populars': popular_movies,
        'all_movies': all_movies,      # ← probably not needed in template
        'randoms': random_movies,
    }

    return render(request, 'home/home.html', context)
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
            return redirect('profile', id=user.id)  # ← redirect to user's own profile
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

@login_required
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