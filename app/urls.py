from django.urls import path
from .views import get_recipes,search_recipes

urlpatterns = [
    path('api/recipes/', get_recipes, name='get_recipes'),
    path('api/search_recipes', search_recipes, name='search_recipes'),
]
