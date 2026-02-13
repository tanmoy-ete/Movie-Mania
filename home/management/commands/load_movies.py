from django.core.management.base import BaseCommand
from home.models import Movie
import pandas as pd

class Command(BaseCommand):
    help = 'Load movies from a CSV file into the database'

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str, help='The path to the CSV file containing movie data')

    def handle(self, *args, **kwargs):
        csv_file = kwargs['csv_file']
        try:
            data = pd.read_csv(csv_file)
            movies = []
            for _, row in data.iterrows():
                movie = Movie(
                    csv_id=row['id'],
                    title=row['title'],
                    overview=row['overview'],
                    genres=row['genres'],
                    keywords=row['keywords'],
                    cast=row['cast'],
                    crew=row['crew'],
                    release_date=row['release_date'],
                    popularity=row['popularity'],
                    runtime=row['runtime'],
                    spoken_languages=row['spoken_languages'],
                    tags=row['tags']
                )
                movies.append(movie)
            Movie.objects.bulk_create(movies)
            self.stdout.write(self.style.SUCCESS(f'Successfully loaded {len(movies)} movies from {csv_file}'))
        except Exception as e:
            self.stderr.write(self.style.ERROR(f'Error loading movies: {e}'))


