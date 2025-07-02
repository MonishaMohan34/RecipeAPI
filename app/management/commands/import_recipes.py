import json
from django.core.management.base import BaseCommand
from app.models import Recipe  # change 'app' to your app name

class Command(BaseCommand):
    help = 'Import recipes from JSON file'

    def handle(self, *args, **kwargs):
        with open("recipes.json", encoding="utf-8") as f:
            data = json.load(f)
            for key, r in data.items():
    # Skip if title is missing
                if not r.get("title"):
                    continue

                try:
                    Recipe.objects.create(
                        cuisine=r.get("cuisine"),
                        title=r.get("title"),
                        rating=float(r["rating"]) if r.get("rating") not in ["NaN", None] else None,
                        prep_time=int(r["prep_time"]) if r.get("prep_time") not in ["NaN", None] else None,
                        cook_time=int(r["cook_time"]) if r.get("cook_time") not in ["NaN", None] else None,
                        total_time=int(r["total_time"]) if r.get("total_time") not in ["NaN", None] else None,
                        description=r.get("description", ""),
                        nutrients=json.dumps(r.get("nutrients", {})),
                        serves=r.get("serves", "N/A")
                    )
                except Exception as e:
                    print(f"❌ Skipping recipe due to error: {e}")

        self.stdout.write(self.style.SUCCESS("✅ Recipes imported successfully."))
