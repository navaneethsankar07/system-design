import json

from django.http import JsonResponse
from django.shortcuts import get_object_or_404

from .cache import redis_client
from .models import Product


def product_detail(request, product_id):
    cache_key = f"product:{product_id}"

    cached_product = redis_client.get(cache_key)

    if cached_product:
        return JsonResponse(json.loads(cached_product))

    product = get_object_or_404(Product, id=product_id)

    product_data = {
        "id": product.id,
        "name": product.name,
        "description": product.description,
        "price": str(product.price),
        "stock": product.stock,
    }

    redis_client.set(cache_key, json.dumps(product_data))

    return JsonResponse(product_data)
