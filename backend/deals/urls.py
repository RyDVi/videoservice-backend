from rest_framework_nested import routers
from django.urls import path, include

from deals.views import DealTypesViewSet, DealsViewSet


def get_deals_router(base_router):
    deals_router = routers.NestedDefaultRouter(base_router, r"deals", lookup="deals")
    deals_router.register(r"deal_type", DealTypesViewSet)
    return deals_router


def get_deals_types_router(base_router):
    deals_types = routers.NestedDefaultRouter(
        base_router, r"deal_types", lookup="deal_types"
    )
    deals_types.register(r"deals", DealsViewSet)
    return deals_types


def deals_url_patterns(base_router, lpath):
    return [
        path(lpath, include(get_deals_router(base_router).urls)),
        path(lpath, include(get_deals_types_router(base_router).urls)),
    ]
