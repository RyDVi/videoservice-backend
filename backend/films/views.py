
from backend.views import (
    FilterBackend,
    OrderingFilter,
    RelatedViewSetsMixin,
    StandardPagination,
)
from films.filters import FilmsFilters, FilmsPersonsFilters, GenresFilters
from films.models import (
    Category,
    Film,
    FilmPrice,
    FilmsCategories,
    FilmsGenres,
    FilmsPersons,
    FilmsUsers,
    Genre,
    Person,
    PersonRole,
)
from films.serializers import (
    CategorySerializer,
    CategoryWithDictsSerializer,
    FilmPriceSerializer,
    FilmsCategoriesSerializer,
    FilmsGenresSerializer,
    FilmsPersonsSerializer,
    FilmSerializer,
    FilmsUsersSerializer,
    GenresSerializer,
    PersonRoleSerializer,
    PersonsSerializer,
)
from organization.base.views import AppModelViewSet
from rest_framework.permissions import DjangoModelPermissionsOrAnonReadOnly
from rest_framework.decorators import action
from rest_framework.response import Response


class FilmsViewSet(RelatedViewSetsMixin, AppModelViewSet):
    permission_classes = [DjangoModelPermissionsOrAnonReadOnly]
    queryset = Film.objects.all()
    serializer_class = FilmSerializer
    pagination_class = StandardPagination
    filterset_class = FilmsFilters
    filter_backends = (
        FilterBackend,
        OrderingFilter,
    )
    ordering_fields = "__all__"

    related_lookups = {
        "user_pk": "users",
        "films_users_pk": "films_users",
        "films_persons_pk": "films_persons",
        "films_genres_pk": "films_genres",
    }

    def filter_queryset(self, queryset):
        return super().filter_queryset(queryset)


class GenresViewSet(RelatedViewSetsMixin, AppModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenresSerializer
    filterset_class = GenresFilters
    filter_backends = (
        FilterBackend,
        OrderingFilter,
    )
    ordering_fields = "__all__"

    related_lookups = {"films_genres_pk": "films_genres"}


class FilmsGenresViewSet(RelatedViewSetsMixin, AppModelViewSet):
    queryset = FilmsGenres.objects.all()
    serializer_class = FilmsGenresSerializer

    related_lookups = {"film_pk": "film", "genre_pk": "genre"}


class PersonRolesViewSet(RelatedViewSetsMixin, AppModelViewSet):
    queryset = PersonRole.objects.all()
    serializer_class = PersonRoleSerializer

    related_lookups = {"person_pk": "person"}


class PersonsViewSet(RelatedViewSetsMixin, AppModelViewSet):
    queryset = Person.objects.all()
    serializer_class = PersonsSerializer

    related_lookups = {"role_pk": "role", "films_persons_pk": "films_persons"}


class FilmsPersonsViewSet(RelatedViewSetsMixin, AppModelViewSet):
    queryset = FilmsPersons.objects.all()
    serializer_class = FilmsPersonsSerializer
    filterset_class = FilmsPersonsFilters
    filter_backends = (
        FilterBackend,
        OrderingFilter,
    )

    related_lookups = {"film_pk": "film", "person_pk": "person"}


class FilmsUsersViewSet(RelatedViewSetsMixin, AppModelViewSet):
    queryset = FilmsUsers.objects.all()
    serializer_class = FilmsUsersSerializer

    related_lookups = {"user_pk": "user", "film_pk": "film"}


class FilmsPricesViewSet(RelatedViewSetsMixin, AppModelViewSet):
    queryset = FilmPrice.objects.all()
    serializer_class = FilmPriceSerializer

    related_lookups = {"film_pk": "film", "deal_type_pk": "deal_type"}


class CategoriesViewSet(RelatedViewSetsMixin, AppModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filter_backends = (
        FilterBackend,
        OrderingFilter,
    )
    ordering_fields = "__all__"

    related_lookups = {"films_categories_pk": "films_categories"}

    @action(methods=['GET'], detail=False)
    def with_dicts(self, request):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = CategoryWithDictsSerializer(
            queryset, many=True, context={"request": request})
        return Response(serializer.data)


class FilmsCategoriesViewSet(RelatedViewSetsMixin, AppModelViewSet):
    queryset = FilmsCategories.objects.all()
    serializer_class = FilmsCategoriesSerializer

    related_lookups = {"film_pk": "film", "category_pk": "category"}
