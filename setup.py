import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'prompt_injector.settings'

from dotenv import load_dotenv
load_dotenv()

import django
django.setup()

import json
import logging

from products.models import Pet, Book, Movie, Flag

def main():
    logger = logging.getLogger("setup")
    # If flag has been set, that means data has been inserted
    if Flag.objects.all().exists():
        logger.info("Data has already been inserted")
        return
    
    with open("data.json", "r") as f:
        data = json.load(f)
    
    logger.info("Inserting pets")
    for pet in data["pets"]:
        Pet.objects.create(**pet)
    
    logger.info("Inserting books")
    for book in data["books"]:
        Book.objects.create(**book)
    
    logger.info("Inserting movies")
    for movie in data["movies"]:
        Movie.objects.create(**movie)
    
    logger.info("Inserting flag")
    Flag.objects.create(value=os.environ.get("FLAG"))


if __name__ == "__main__":
    main()
