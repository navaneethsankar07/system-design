from django.http import JsonResponse
from django.shortcuts import get_object_or_404

from .models import Product


def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    return JsonResponse(
        {
            "id": product.id,
            "name": product.name,
            "description": product.description,
            "price": str(product.price),
            "stock": product.stock,
        }
    )
