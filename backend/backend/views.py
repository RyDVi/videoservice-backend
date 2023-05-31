from rest_framework.pagination import PageNumberPagination
from django_filters import rest_framework as django_filters
from rest_framework import filters

class StandardPagination(PageNumberPagination):
    page_size = 100
    page_size_query_param = "page_size"
    max_page_size = 1000
    
class OrderingFilter(filters.OrderingFilter):
    pass

class FilterBackend(django_filters.DjangoFilterBackend):
    pass


class RelatedViewSetsMixin:
    """
    For nested viewsets. Will be filter nested entries
    In related_lookups:
    1) in key set getting from request id of entry
    2) in value set filter name
    """

    related_lookups = {}

    def get_queryset(self):
        kwargs = self.request.parser_context["kwargs"]
        queryset = super().get_queryset()
        for lookup in self.related_lookups:
            if kwargs.get(lookup, None):
                queryset = queryset.filter(
                    **{self.related_lookups[lookup]: kwargs[lookup]}
                )
        return queryset
