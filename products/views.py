from django.http import HttpRequest, JsonResponse

from .models import Pet, Book, Movie, Flag

def get_all_products(request: HttpRequest):
    pets = list(Pet.objects.values())
    books = list(Book.objects.values())
    movies = list(Movie.objects.values())
    return JsonResponse({
        "pets": pets,
        "books": books,
        "movies": movies,
    })
