from django.shortcuts import render

# Create your views here.
from django.core.paginator import Paginator
from django.http import JsonResponse
from .models import Recipe
import json
def index_page(request):
    return render(request, 'index.html') 
def get_recipes(request):
    page = int(request.GET.get("page", 1))
    limit = int(request.GET.get("limit", 10))

    recipes = Recipe.objects.all().order_by("-rating")
    paginator = Paginator(recipes, limit)
    page_obj = paginator.get_page(page)

    data = []
    for rec in page_obj:
        data.append({
            "id": rec.id,
            "title": rec.title,
            "cuisine": rec.cuisine,
            "rating": rec.rating,
            "prep_time": rec.prep_time,
            "cook_time": rec.cook_time,
            "total_time": rec.total_time,
            "description": rec.description[:80] + "...",
            "nutrients": json.loads(rec.nutrients),
            "serves": rec.serves,
        })

    return JsonResponse({
        "page": page,
        "limit": limit,
        "total": paginator.count,
        "data": data
    })



def search_recipes(request):
    title = request.GET.get("title", "")
    rating = request.GET.get("rating", None)
    cuisine = request.GET.get("cuisine", "")
    calories = request.GET.get("calories", None)

    queryset = Recipe.objects.all()

    # Apply filters
    if title:
        queryset = queryset.filter(title__icontains=title)
    if cuisine:
        queryset = queryset.filter(cuisine__icontains=cuisine)
    if rating:
        try:
            queryset = queryset.filter(rating__gte=float(rating))
        except ValueError:
            return JsonResponse({"error": "Invalid rating value"}, status=400)

    result = []
    for rec in queryset:
        try:
            nutrients = json.loads(rec.nutrients)
            if calories:
                cal = nutrients.get("calories", "0 kcal").split()[0]
                if float(cal) > float(calories):
                    continue
        except Exception:
            continue  # skip recipe if nutrients parsing fails

        result.append({
            "id": rec.id,
            "title": rec.title,
            "cuisine": rec.cuisine,
            "rating": rec.rating,
            "prep_time": rec.prep_time,
            "cook_time": rec.cook_time,
            "total_time": rec.total_time,
            "description": rec.description[:80] + "...",
            "nutrients": nutrients if rec.nutrients else {},
            "serves": rec.serves
        })

    return JsonResponse({"data": result})

