import datetime
from django.db import models
from django.contrib.auth.models import User
from django.core import validators
from django.utils.translation import gettext_lazy as _
from deals.models import DealType
from films.constants import CONTENT_RATING_CHOICES, FILM_TYPE_CHOICES, ContentRating, FilmType
from films.managers import FilmsQuerySet, GenresQuerySet

from organization.base.models import AppOrgModel, SlugFieldMixin
from backend.models import BaseAppModel, image_storage
from django_countries.fields import CountryField


class PersonRole(AppOrgModel):
    """For example: producer, actor, operator"""

    name = models.CharField(verbose_name=_("name"), max_length=255, blank=True)

    class Meta:
        db_table = "person_roles"
        constraints = [
            models.UniqueConstraint(
                fields=["name", "org"], name="unique roles by org")
        ]


class Person(AppOrgModel):
    firstname = models.CharField(
        verbose_name=_("firstname"), max_length=255, blank=True
    )
    lastname = models.CharField(verbose_name=_(
        "lastname"), max_length=255, blank=True)

    class Meta:
        db_table = "persons"
        constraints = [
            models.UniqueConstraint(
                fields=["firstname", "lastname", "org"], name="unique person by org"
            )
        ]


class Category(AppOrgModel, SlugFieldMixin):
    name = models.CharField(max_length=255, verbose_name=_("genre of film"))

    class Meta:
        db_table = "categories"
        constraints = [
            models.UniqueConstraint(
                fields=["org", "name"], name="unique category by org")
        ]

class Genre(AppOrgModel, SlugFieldMixin):
    name = models.CharField(max_length=255, verbose_name=_("genre of film"))
    objects = GenresQuerySet.as_manager()

    class Meta:
        db_table = "genres"
        constraints = [
            models.UniqueConstraint(
                fields=["org", "name"], name="unique genre by org")
        ]

class Film(AppOrgModel, SlugFieldMixin):
    image = models.ImageField(verbose_name=_(
        "film image"), storage=image_storage, null=True)
    name = models.CharField(verbose_name=_("film name"), max_length=256)
    original_name = models.CharField(
        verbose_name=_("original film name"), max_length=256)
    description_full = models.TextField(verbose_name=_("film description"))
    description_short = models.TextField(
        verbose_name=_("film short description"))
    country = CountryField(verbose_name=_(
        "film country"), blank=True, null=True)
    content_rating = models.PositiveSmallIntegerField(
        verbose_name=_("film content rating by content rating system"),
        choices=CONTENT_RATING_CHOICES,
        default=ContentRating.ZERO,
    )
    genres = models.ManyToManyField(
        Genre,
        through="FilmsGenres",
        related_name="films",
        verbose_name=_("genres of film"),
    )
    categories = models.ManyToManyField(
        Category,
        through="FilmsCategories",
        related_name="films",
        verbose_name=_("categories of film")
    )
    users = models.ManyToManyField(
        User, verbose_name=_("users films"), related_name="films", through="FilmsUsers"
    )
    persons = models.ManyToManyField(
        Person,
        verbose_name=_("Persons involved in the making of the film"),
        related_name="films",
        through="FilmsPersons",
    )
    year = models.PositiveIntegerField(default=datetime.datetime.now().year)
    type = models.CharField(
        choices=FILM_TYPE_CHOICES, default=FilmType.FILM, verbose_name=_("type of film"), max_length=6)

    objects = FilmsQuerySet.as_manager()

    class Meta:
        db_table = "films"


class FilmPrice(AppOrgModel):
    """Prices for films"""

    film = models.ForeignKey(
        Film, related_name="prices", on_delete=models.CASCADE)
    type = models.ForeignKey(
        DealType, related_name="prices", on_delete=models.CASCADE)
    price = models.DecimalField(decimal_places="2", max_digits=20)

    class Meta:
        db_table = "film_prices"
        constraints = [
            models.UniqueConstraint(
                fields=["film", "type", "org"],
                name="unique by film, price type and org",
            )
        ]


class FilmsUsers(BaseAppModel):
    tenant_link = "film__org"
    user = models.ForeignKey(
        User, related_name="films_users", on_delete=models.CASCADE)
    film = models.ForeignKey(
        Film, related_name="films_users", on_delete=models.CASCADE)
    rating = models.PositiveSmallIntegerField(
        default=None,
        null=True,
        validators=[validators.MinValueValidator(
            1), validators.MaxValueValidator(100)],
    )
    bookmark = models.BooleanField(
        verbose_name=_("added to bookmarks"), default=False)

    class Meta:
        db_table = "films_users"
        unique_together = ("film", "user")


class FilmsPersons(BaseAppModel):
    tenant_link = "film__org"
    person = models.ForeignKey(
        Person, related_name="films_persons", on_delete=models.CASCADE
    )
    film = models.ForeignKey(
        Film, related_name="films_persons", on_delete=models.CASCADE
    )
    role = models.ForeignKey(
        PersonRole, related_name="person", on_delete=models.CASCADE
    )

    class Meta:
        db_table = "films_persons"
        unique_together = ("film", "person", "role")

class FilmsGenres(BaseAppModel):
    film = models.ForeignKey(
        Film, related_name="films_genres", on_delete=models.CASCADE
    )
    genre = models.ForeignKey(
        Genre, related_name="films_genres", on_delete=models.CASCADE
    )

    class Meta:
        db_table = "films_genres"
        unique_together = ("film", "genre")

class FilmsCategories(BaseAppModel):
    tenant_link = "film__org"
    film = models.ForeignKey(
        Film, related_name="films_categories", on_delete=models.CASCADE
    )
    category = models.ForeignKey(
        Category, related_name="films_categories", on_delete=models.CASCADE
    )

    class Meta:
        db_table = "films_categories"
        unique_together = ("category", "film")
