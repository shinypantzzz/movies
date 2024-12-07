from uuid import uuid4

from django.db import models
from django.contrib.auth import models as auth_models

# Create your models here.

class Movie(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=300)

class User(auth_models.AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    favorite_movies = models.ManyToManyField(Movie)
