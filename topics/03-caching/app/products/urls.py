from django.urls import path

from .views import product_detail, update_product, update_product_write_through

urlpatterns = [
    path(
        "products/<int:product_id>/",
        product_detail,
        name="product-detail",
    ),
    path(
        "products/<int:product_id>/update/",
        update_product,
        name="update-product",
    ),
    path(
        "products/<int:product_id>/write-through/",
        update_product_write_through,
        name="update-product-write-through",
    ),
]
