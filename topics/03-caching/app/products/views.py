import json
import os
from django.http import JsonResponse
from django.shortcuts import get_object_or_404

from django.db import transaction
from django.views.decorators.csrf import csrf_exempt
from .cache import CACHE_TTL, redis_client
from .models import Product


import random

NOT_FOUND = "__NOT_FOUND__"
NEGATIVE_CACHE_TTL = 30
TTL_JITTER = int(os.getenv("CACHE_TTL_JITTER", 30))


def product_detail(request, product_id):
    cache_key = f"product:{product_id}"

    cached_product = redis_client.get(cache_key)

    if cached_product is not None:
        if cached_product == NOT_FOUND:
            response = JsonResponse(
                {"error": "Product not found"},
                status=404,
            )
            response["X-Cache"] = "HIT"
            return response

        response = JsonResponse(json.loads(cached_product))
        response["X-Cache"] = "HIT"
        return response
    try:
        product = Product.objects.get(id=product_id)
    except Product.DoesNotExist:
        redis_client.setex(
            cache_key,
            NEGATIVE_CACHE_TTL,
            NOT_FOUND,
        )

        response = JsonResponse(
            {"error": "Product not found"},
            status=404,
        )
        response["X-Cache"] = "MISS"
        return response

    product_data = {
        "id": product.id,
        "name": product.name,
        "description": product.description,
        "price": str(product.price),
        "stock": product.stock,
    }

    ttl = CACHE_TTL + random.randint(0, TTL_JITTER)

    redis_client.setex(
        cache_key,
        ttl,
        json.dumps(product_data),
    )

    response = JsonResponse(product_data)
    response["X-Cache"] = "MISS"

    return response


@csrf_exempt
def update_product(request, product_id):
    if request.method != "POST":
        return JsonResponse(
            {"error": "Only POST is allowed"},
            status=405,
        )

    try:
        data = json.loads(request.body)
        new_price = data["price"]
    except (json.JSONDecodeError, KeyError, TypeError):
        return JsonResponse(
            {"error": "A valid price is required"},
            status=400,
        )

    try:
        with transaction.atomic():
            product = Product.objects.select_for_update().get(id=product_id)
            product.price = new_price
            product.save(update_fields=["price"])

            transaction.on_commit(lambda: redis_client.delete(f"product:{product_id}"))

    except Product.DoesNotExist:
        return JsonResponse(
            {"error": "Product not found"},
            status=404,
        )

    return JsonResponse(
        {
            "message": "Product updated",
            "id": product.id,
            "price": str(product.price),
        }
    )


@csrf_exempt
def update_product_write_through(request, product_id):
    if request.method != "POST":
        return JsonResponse(
            {"error": "Only POST is allowed"},
            status=405,
        )

    try:
        data = json.loads(request.body)
        new_price = data["price"]
    except (json.JSONDecodeError, KeyError, TypeError):
        return JsonResponse(
            {"error": "A valid price is required"},
            status=400,
        )

    try:
        with transaction.atomic():
            product = Product.objects.select_for_update().get(id=product_id)
            product.price = new_price
            product.save(update_fields=["price"])

            product_data = {
                "id": product.id,
                "name": product.name,
                "description": product.description,
                "price": str(product.price),
                "stock": product.stock,
            }

            transaction.on_commit(
                lambda: redis_client.setex(
                    f"product:{product_id}",
                    CACHE_TTL,
                    json.dumps(product_data),
                )
            )

    except Product.DoesNotExist:
        return JsonResponse(
            {"error": "Product not found"},
            status=404,
        )

    return JsonResponse(
        {
            "message": "Product updated using write-through",
            "product": product_data,
        }
    )
