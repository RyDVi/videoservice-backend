from django.urls import include, path
from rest_framework_nested import routers

from films.views import FilmsUsersViewSet, FilmsViewSet
from leads.views import LeadsViewSet


def get_users_router(base_router):
    users_router = routers.NestedDefaultRouter(base_router, r"users", lookup="user")
    users_router.register(r"films", FilmsViewSet)
    users_router.register(r"films_users", FilmsUsersViewSet)
    return users_router


def get_customers_router(base_router):
    customer_router = routers.NestedDefaultRouter(
        base_router, r"customers", lookup="customer"
    )
    customer_router.register(r"lead", LeadsViewSet)
    return customer_router


def users_url_patterns(base_router, lpath):
    return [
        path(lpath, include(get_users_router(base_router).urls)),
        path(lpath, include(get_customers_router(base_router).urls)),
    ]
