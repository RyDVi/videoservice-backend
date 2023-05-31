import django_filters
from backend.filters import CharInFilter
from django_filters.rest_framework import FilterSet

from films.services import get_films_names_using_gpt


class FilmsFilters(FilterSet):
    slug = CharInFilter()
    search = django_filters.CharFilter(field_name="search", method="do_search")
    category = CharInFilter(method="filter_by_category")
    genre = CharInFilter(method="filter_by_genre")
    year = CharInFilter(field_name="year")
    country = CharInFilter(method="filter_by_country")

    def do_search(self, queryset, name, value):
        query = queryset.search(value)
        if query.count()>0:
            return query
        
        possible_films = get_films_names_using_gpt(value)
        print(possible_films)
        if not len(possible_films):
            return query.none()
        query = query.none()
        for possible_film in possible_films:
            query = query | queryset.search(possible_film)
        return query.distinct()

    def filter_by_category(self, queryset, name, value):
        return queryset.category(value)

    def filter_by_genre(self, queryset, name, value):
        return queryset.genre(value)

    def filter_by_country(self, queryset, name, value):
        return queryset.country(value)


class GenresFilters(FilterSet):
    category = django_filters.CharFilter(method="filter_by_category")
    
    
    def filter_by_category(self, queryset, name, value):
        return queryset.exists_in_films_by_category(value)
    
    
class FilmsPersonsFilters(FilterSet):
    film = django_filters.UUIDFilter(field_name="film")