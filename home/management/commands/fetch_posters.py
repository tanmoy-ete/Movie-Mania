from django.core.management.base import BaseCommand
from home.models import Movie
from home.utils import fetch_poster


class Command(BaseCommand):
    help = "Fetch and store posters for all movies"

    def handle(self, *args, **kwargs):
        movies = Movie.objects.filter(poster_url__isnull=True)
        total = movies.count()

        if total == 0:
            self.stdout.write(self.style.WARNING("No movies are missing posters"))
            return

        self.stdout.write(f"Fetching posters for {total} movies...")

        count = 0
        for index, movie in enumerate(movies, start=1):
            self.stdout.write(f"[{index}/{total}] Fetching poster for: {movie.title}")
            poster = fetch_poster(movie.csv_id)
            if poster:
                movie.poster_url = poster
                movie.save()
                count += 1
                self.stdout.write(self.style.SUCCESS(f"[{index}/{total}] Saved: {movie.title}"))
            else:
                self.stdout.write(self.style.WARNING(f"[{index}/{total}] No poster found for: {movie.title}"))

        self.stdout.write(self.style.SUCCESS(f"{count} posters saved"))
