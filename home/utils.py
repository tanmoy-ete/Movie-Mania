import pickle
import requests
from .models import Movie
import pandas as pd 
from django.conf import settings
import os
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer


BASE_DIR = settings.BASE_DIR




def fetch_poster(csv_id):
    try:
        url = f"https://api.themoviedb.org/3/movie/{csv_id}?api_key=0b29be5d256cf9b3724fdc3a88587274&language=en-US"
        
        response = requests.get(url, timeout=10)
        data = response.json()

        poster_path = data.get('poster_path')

        if poster_path:
            return "https://image.tmdb.org/t/p/w500" + poster_path
        else:
            return None

    except Exception as e:
        print(f"Error fetching poster for ID {csv_id}: {e}")
        return None



def recommendation(id):
    recommendations = []

    movies = Movie.objects.all()
    all_movies = pd.DataFrame(list(movies.values()))


    cv = CountVectorizer(max_features=5000, stop_words='english')
    vectors = cv.fit_transform(all_movies['tags']).toarray()
    similarity = cosine_similarity(vectors)

    movie_index = all_movies[all_movies['id'] == id].index[0]
    distances = similarity[movie_index]

    movies_list = sorted(enumerate(distances), reverse=True, key=lambda x:x[1])[1:25]

    for i in movies_list:
        recommended_movie = Movie.objects.get(id=all_movies.iloc[i[0]]['id'])
        recommendations.append(recommended_movie)

    return recommendations