from rest_framework_nested import routers
from films.views import (
    FilmsGenresViewSet,
    FilmsPersonsViewSet,
    FilmsUsersViewSet,
    FilmsViewSet,
    PersonRolesViewSet,
    PersonsViewSet,
)

from users.views import UsersViewSet
from django.urls import include, path


def get_films_router(base_router):
    films_router = routers.NestedDefaultRouter(base_router, r"films", lookup="film")
    films_router.register(r"users", UsersViewSet)
    films_router.register(r"films_users", FilmsUsersViewSet)
    films_router.register(r"films_persons", FilmsPersonsViewSet)
    films_router.register(r"films_genres", FilmsGenresViewSet)
    return films_router


def get_films_users_router(base_router):
    films_users_router = routers.NestedDefaultRouter(
        base_router, r"films_users", lookup="films_users"
    )
    films_users_router.register(r"user", UsersViewSet)
    films_users_router.register(r"film", FilmsViewSet)
    return films_users_router


def get_persons_router(base_router):
    persons_router = routers.NestedDefaultRouter(
        base_router, r"persons", lookup="persons"
    )
    persons_router.register(r"films", FilmsViewSet)
    persons_router.register(r"films_persons", FilmsPersonsViewSet)
    persons_router.register(r"person_roles", PersonRolesViewSet)
    return persons_router


def get_person_roles_router(base_router):
    person_roles_router = routers.NestedDefaultRouter(
        base_router, r"person_roles", lookup="person_roles"
    )
    person_roles_router.register(r"persons", PersonsViewSet)
    return person_roles_router


def get_genres_router(base_router):
    genres_router = routers.NestedDefaultRouter(base_router, r"genres", lookup="genres")
    genres_router.register(r"films", FilmsViewSet)
    genres_router.register(r"films_genres", FilmsGenresViewSet)
    return genres_router

def film_url_patterns(base_router, lpath):
    return [
        path(lpath, include(get_films_router(base_router).urls)),
        path(lpath, include(get_films_users_router(base_router).urls)),
        path(lpath, include(get_persons_router(base_router).urls)),
        path(lpath, include(get_person_roles_router(base_router).urls)),
        path(lpath, include(get_genres_router(base_router).urls)),
    ]
