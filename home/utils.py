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



df = None
vectors = None
cv = None

def load_data():
    global df, vectors, cv

    movies = Movie.objects.all()
    df = pd.DataFrame(list(movies.values()))

    if df.empty:
        return


    cv = CountVectorizer(max_features=2000, stop_words='english')
    vectors = cv.fit_transform(df['tags'])

# Load once at startup
try:
    load_data()
except Exception as e:
    print("Startup load failed:", e)


def recommendation(movie_id):
    global df, vectors

    if df is None or vectors is None:
        return []

    if movie_id not in df['id'].values:
        return []

    movie_index = df[df['id'] == movie_id].index[0]

    similarity_scores = cosine_similarity(
        vectors[movie_index],
        vectors
    ).flatten()

    similar_indices = similarity_scores.argsort()[-25:][::-1][1:]

    recommendations = []

    for i in similar_indices:
        recommendations.append(
            Movie.objects.get(id=df.iloc[i]['id'])
        )

    return recommendations