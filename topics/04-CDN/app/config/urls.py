from django.urls import include, path

urlpatterns = [
    path("api/", include("cdn_demo.urls")),
]
