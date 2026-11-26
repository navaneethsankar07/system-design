import json

from django.http import JsonResponse
from django.shortcuts import get_object_or_404

from django.db import transaction
from django.views.decorators.csrf import csrf_exempt
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
