import django_filters
from backend.filters import CharInFilter
from django_filters.rest_framework import FilterSet


class VideoFilters(FilterSet):
    film = django_filters.UUIDFilter(field_name="film")