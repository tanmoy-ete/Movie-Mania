import ast
from .models import Movie
import pycountry


def global_genres(request):
    movies = Movie.objects.only('genres')
    genre_set = set()
    for movie in movies:
        if movie.genres:
            try:
                genres_list = ast.literal_eval(movie.genres)
                for genre in genres_list:
                    genre_set.add(genre.strip())
            except:
                continue
    return {
        'all_genres' : sorted(list(genre_set))
    }

def global_lang(request):
    lang_set = set()

    
    movies = Movie.objects.only('spoken_languages')

    for movie in movies:
        if movie.spoken_languages:
            try:
                lang_list = ast.literal_eval(movie.spoken_languages)
                lang_set.update(lang_list)  # add all at once
            except (ValueError, SyntaxError):
                continue

    language_data = []

    for code in sorted(lang_set):
        code = code.strip()

        try:
            language = pycountry.languages.get(alpha_2=code)
            name = language.name if language else code.upper()
        except:
            name = code.upper()

        language_data.append({
            'code': code,
            'name': name
        })

    return {
        'all_langs': language_data
    }