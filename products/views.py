from django.db import connection, models
from django.http import HttpRequest, JsonResponse
from django.views.decorators.http import require_http_methods
import logging
from typing import Type

from .models import Pet, Book, Movie, Flag
from .agents import Agent, QueryException

logger = logging.getLogger("products.views")
tables: list[Type[models.Model]] = [Pet, Book, Movie, Flag]

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

def _table_exists(table_name: str):
    with connection.cursor() as cursor:
        table_names = connection.introspection.table_names(cursor)
        return table_name in table_names

def _get_model_class(table_name: str):
    for table in tables:
        if table.objects.model._meta.db_table == table_name:
            return table

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
        table_names.append(name.strip())
    logger.info(f"Table names: {table_names}")
    
    # Get filters from query
    try:
        filter_response = Agent("field").query(query=query)
    except QueryException as e:
        logger.error(f"Query exception: {e}")
        return JsonResponse({"error": "LLM error"}, status=400)
    
    # Extract filters from response
    logger.info(f"Filter response:\n{filter_response}")
    filters = dict()
    skipped_lines = ["", "```json", "```"]
    for line in filter_response.split("\n"):
        line = line.strip()
        if line in skipped_lines:
            continue
        line_split = line.split("=")
        if len(line_split) != 2:
            logger.error(f"Invalid filter line: \"{line}\"")
            return JsonResponse({"error": "LLM response format error"}, status=400)
        field_name, field_value = line_split
        field_name = field_name.strip()
        field_value = field_value.strip()
        if field_value.lower() == "none":
            continue
        filters[field_name] = field_value
    
    # Do DB queries and obtain results
    logger.info(f"Filters: {filters}")
    objects = []
    for table_name in table_names:
        model = _get_model_class(f"products_{table_name}")
        if model is None:
            continue
        try:
            new_objects = list(model.objects.filter(**filters).values())
        except Exception as e:
            logger.error(f"DB filter exception: {e}")
            continue
        objects.extend(new_objects)
    
    return JsonResponse({"values": objects})
