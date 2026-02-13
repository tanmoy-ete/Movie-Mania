from django.urls import path
from django.contrib.auth.views import LoginView
from . import views

urlpatterns = [
    path('', views.movies, name='movies'),
    path('registration/', views.register, name='registration'),
    path('login/', LoginView.as_view(template_name='home/login.html',redirect_authenticated_user=True,), name='login'),
    path("search/", views.search_movies, name="search_movie"),
    path('movie/<int:id>/', views.movie_detail, name='movie_detail'),
    path('profile/<int:id>/', views.profile, name='profile'),
    path('logout/', views.user_logout, name='logout'),
    path('genres/<str:genres>', views.get_movies_by_genres, name='movie_genres'),
    path('languages/<str:spoken_languages>', views.get_movies_by_langs, name='movie_lang'),
    path('download-link/', views.download, name='download'),
]
