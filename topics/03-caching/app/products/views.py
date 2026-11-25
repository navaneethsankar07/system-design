import json

from django.http import JsonResponse
from django.shortcuts import get_object_or_404

from .cache import CACHE_TTL, redis_client
from .models import Product


def product_detail(request, product_id):
    cache_key = f"product:{product_id}"

    cached_product = redis_client.get(cache_key)

    if cached_product is not None:
        response = JsonResponse(json.loads(cached_product))
        response["X-Cache"] = "HIT"
        return response

    product = get_object_or_404(Product, id=product_id)

    product_data = {
        "id": product.id,
        "name": product.name,
        "description": product.description,
        "price": str(product.price),
        "stock": product.stock,
    }

    redis_client.setex(
        cache_key,
        CACHE_TTL,
        json.dumps(product_data),
    )

    response = JsonResponse(product_data)
    response["X-Cache"] = "MISS"

    return response
