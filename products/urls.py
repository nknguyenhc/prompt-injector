from django.urls import path

from .views import get_all_products, prompt

urlpatterns = [
    path("all/", view=get_all_products),
    path("prompt/", view=prompt),
]
