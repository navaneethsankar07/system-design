from datetime import datetime, timezone
from django.http import JsonResponse


PRODUCTS = [
    {"id": 1, "name": "Laptop", "price": 65000},
    {"id": 2, "name": "Keyboard", "price": 2500},
    {"id": 3, "name": "Mouse", "price": 1200},
    {"id": 4, "name": "Monitor", "price": 18000},
]


def products(request):
    response = JsonResponse({
        "source": "django-origin",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "products": PRODUCTS,
    })

    # This is a public, cacheable response for the CDN demonstration.
    response["Cache-Control"] = "public, max-age=30"
    return response


def health(request):
    response = JsonResponse({
        "status": "healthy",
        "source": "django-origin",
    })
    response["Cache-Control"] = "no-store"
    return response
