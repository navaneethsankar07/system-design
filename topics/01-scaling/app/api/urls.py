from django.urls import path

from . import views

urlpatterns = [
    path("health/", views.health, name="health"),
    path("info/", views.server_info, name="server-info"),
    path("light/", views.light_work, name="light-work"),
    path("work/", views.cpu_work, name="cpu-work"),
]
