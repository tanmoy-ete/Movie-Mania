from django.core.management.base import BaseCommand
from home.models import Movie
from home.utils import fetch_poster


class Command(BaseCommand):
    help = "Fetch and store posters for all movies"

    def handle(self, *args, **kwargs):
        movies = Movie.objects.filter(poster_url__isnull=True)

        count = 0
        for movie in movies:
            poster = fetch_poster(movie.csv_id)
            if poster:
                movie.poster_url = poster
                movie.save()
                count += 1
                print(f"Saved: {movie.title}")
            else:
                print(f"No poster found for: {movie.title}")

        self.stdout.write(self.style.SUCCESS(f"{count} posters saved"))
