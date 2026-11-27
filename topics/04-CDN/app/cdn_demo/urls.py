from django.urls import path
from . import views

urlpatterns = [
    path("products/", views.products, name="products"),
    path("health/", views.health, name="health"),
]
