from django.db import connection
from django.http import HttpRequest, JsonResponse
from django.views.decorators.http import require_http_methods
import logging

from .models import Pet, Book, Movie, Flag
from .agents import Agent, QueryException

logger = logging.getLogger("products.views")

@require_http_methods(["GET"])
def get_all_products(request: HttpRequest):
    pets = list(Pet.objects.values())
    books = list(Book.objects.values())
    movies = list(Movie.objects.values())
    return JsonResponse({
        "pets": pets,
        "books": books,
        "movies": movies,
    })

def _table_exists(table_name):
    with connection.cursor() as cursor:
        table_names = connection.introspection.table_names(cursor)
        return table_name in table_names

@require_http_methods(["GET"])
def prompt(request: HttpRequest):
    # Query parameter is required
    query = request.GET.get("query", None)
    if query is None:
        logger.info("No query parameter provided")
        return JsonResponse({"error": "No query parameter provided"}, status=400)
    
    # Get table name from query
    try:
        table_response = Agent("table").query(query=query)
    except QueryException as e:
        logger.error(f"Query exception: {e}")
        return JsonResponse({"error": "LLM error"}, status=400)
    
    # Extract table names from response
    table_names: list[str] = []
    for name in table_response.split("\n"):
        if not _table_exists(f"products_{name.strip()}"):
            logger.info(f"Invalid table name: \"{name.strip()}\"")
            break
        table_names.append(name)
    logger.info(f"Table names: {table_names}")
    return JsonResponse({"tables": table_names})
