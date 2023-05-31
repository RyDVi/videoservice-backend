from organization.base.models import OrgQuerySet
from django.db.models import Q


class FilmsQuerySet(OrgQuerySet):
    def search(self, value):
        searched_by_name = self.search_by_name(value)
        searched_by_description = self.search_by_description(value)
        searched_by_persons = self.search_by_persons(value)
        return (searched_by_name | searched_by_description | searched_by_persons).distinct()

    def search_by_description(self, value):
        return self.filter(Q(description_full__icontains=value) | Q(description_short__icontains=value))

    def search_by_name(self, value):
        return self.filter(Q(name__icontains=value) | Q(original_name__icontains=value))

    def search_by_persons(self, value):
        return self.filter(Q(persons__firstname__icontains=value) | Q(persons__lastname__icontains=value))

    def category(self, values):
        l_values = values
        if type(values) == str:
            l_values = [l_values]

        query = self.none()
        for value in l_values:
            query |= self.filter(categories__slug__iexact=value)
        return query

    def genre(self, values):
        query = self.none()
        for value in values:
            query |= self.filter(genres__slug__iexact=value)
        return query

    def country(self, values):
        query = self.none()
        for value in values:
            query |= self.filter(country__iexact=value)
        return query


class GenresQuerySet(OrgQuerySet):
    def exists_in_films_by_category(self, value):
        return self.filter(films__categories__name__iexact=value)
