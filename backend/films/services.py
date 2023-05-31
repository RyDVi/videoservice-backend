import typing
from backend.utils import slugify
from films.models import Category, Genre
from django.conf import settings
import openai

def create_genres_from_names(*,org=None, genre_names: typing.List[str]):
    genres = []
    for genre_name in genre_names:
        genres.append(Genre(org=org, name=genre_name, slug=slugify(genre_name)))
    
    return Genre.objects.bulk_create(genres)

def create_categories_from_names(*, org=None, category_names: typing.List[str]):
    categories = []
    for category_name in category_names:
        categories.append(Category(org=org, name=category_name, slug=slugify(category_name)))

    return Category.objects.bulk_create(categories)


def get_films_names_using_gpt(search: str):
    if not settings.OPENAI_API_KEY:
        return []
    openai.api_key = settings.OPENAI_API_KEY
    
    prompt = f"Search for films with the following description: {search}"
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=prompt,
        max_tokens=100,
        n=5,
        stop=None,
        temperature=0.5,
    )

    films = []
    for choice in response.choices:
        film_text = choice.text.strip()
        film_name = film_text.split("(")[0].strip()
        film_parts = film_name.split(":")
        if len(film_parts) > 1:
            films.extend(film_parts)
        else:
            films.append(film_name)
    return films
    
    