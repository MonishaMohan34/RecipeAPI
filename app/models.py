from django.db import models

from django.db.models import JSONField # For PostgreSQL
# For SQLite, use TextField to store JSON string

class Recipe(models.Model):
    cuisine = models.CharField(max_length=100)
    title = models.CharField(max_length=200)
    rating = models.FloatField(null=True, blank=True)
    prep_time = models.IntegerField(null=True, blank=True)
    cook_time = models.IntegerField(null=True, blank=True)
    total_time = models.IntegerField(null=True, blank=True)
    description = models.TextField()
    nutrients = models.TextField()  # Store JSON as string for SQLite
    serves = models.CharField(max_length=100)
