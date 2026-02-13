from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class CustomUser(AbstractUser):
    phone = models.CharField(max_length=15)
    address = models.TextField()
    interests = models.CharField()


class Movie(models.Model):
    csv_id = models.IntegerField()
    title = models.CharField(max_length=255)
    overview = models.CharField()
    genres = models.CharField(max_length=100)
    keywords = models.CharField()
    cast = models.CharField()
    crew = models.CharField()
    release_date = models.DateField()
    popularity = models.FloatField()
    runtime = models.IntegerField()
    spoken_languages = models.CharField()
    tags = models.CharField()
    poster_url = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.title
    