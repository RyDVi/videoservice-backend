from films.models import (
    Category,
    Film,
    FilmsCategories,
    FilmsGenres,
    FilmsPersons,
    FilmsUsers,
    Genre,
    Person,
    PersonRole,
    FilmPrice,
)
from organization.base.serializers import (
    AppModelSerializer,
    AppOrgModelSerializer,
    AppPrimaryKeyRelatedField,
    DictionarySerializer,
)
from rest_framework import serializers
from drf_extra_fields.fields import Base64ImageField


class FilmSerializer(DictionarySerializer):
    country = serializers.CharField(allow_blank=True)
    image = Base64ImageField(represent_in_base64=False, required=False)
    categories = AppPrimaryKeyRelatedField(
        queryset=Category.objects.all(), many=True
    )
    genres = AppPrimaryKeyRelatedField(
        queryset=Genre.objects.all(), many=True
    )

    class Meta(DictionarySerializer.Meta):
        model = Film
        read_only_fields = ("slug",)
        fields = read_only_fields+DictionarySerializer.Meta.fields + (
            "image",
            "description_full",
            "description_short",
            "country",
            "content_rating",
            "users",
            "persons",
            "original_name",
            "year",
            "categories",
            "genres",
            "type"
        )
        kwargs = {"original_name": {"allow_blank": False}}


class PersonRoleSerializer(DictionarySerializer):
    class Meta(DictionarySerializer.Meta):
        model = PersonRole
        fields = DictionarySerializer.Meta.fields


class PersonsSerializer(AppOrgModelSerializer):
    class Meta(AppOrgModelSerializer.Meta):
        model = Person
        fields = AppOrgModelSerializer.Meta.fields + (
            "firstname",
            "lastname",
        )


class FilmsPersonsSerializer(AppModelSerializer):
    role = AppPrimaryKeyRelatedField(queryset=PersonRole.objects.all())

    class Meta(AppModelSerializer.Meta):
        model = FilmsPersons
        fields = AppModelSerializer.Meta.fields + (
            "film",
            "person",
            "role"
        )


class FilmsUsersSerializer(AppOrgModelSerializer):
    class Meta(AppOrgModelSerializer.Meta):
        model = FilmsUsers
        fields = AppOrgModelSerializer.Meta.fields + (
            "user",
            "film",
            "rating",
            "bookmark",
        )


class FilmPriceSerializer(AppOrgModelSerializer):
    class Meta(AppOrgModelSerializer.Meta):
        model = FilmPrice
        fields = AppOrgModelSerializer.Meta.fields + ("film", "type", "price")


class FilmsCategoriesSerializer(AppOrgModelSerializer):
    class Meta(AppOrgModelSerializer.Meta):
        model = FilmsCategories
        fields = AppOrgModelSerializer.Meta.fields + (
            "film",
            "category",
        )


class CategorySerializer(AppOrgModelSerializer):
    class Meta(AppOrgModelSerializer.Meta):
        model = Category
        read_only_fields = ("slug",)
        fields = read_only_fields+AppOrgModelSerializer.Meta.fields + ("name", )


class CategoryWithDictsSerializer(CategorySerializer):
    genres = serializers.SerializerMethodField()
    countries = serializers.SerializerMethodField()
    years = serializers.SerializerMethodField()

    class Meta(CategorySerializer.Meta):
        read_only_fields = ("genres", "countries", "years",)
        fields = read_only_fields + CategorySerializer.Meta.fields

    def get_years(self, obj):
        return list(obj.films.all().values_list('year', flat=True).distinct())

    def get_countries(self, obj):
        return list(obj.films.all().values_list('country', flat=True).distinct())

    def get_genres(self, obj):
        return list(obj.films.filter(genres__isnull=False).values_list('genres', flat=True).distinct())


class FilmsGenresSerializer(AppOrgModelSerializer):
    class Meta(AppOrgModelSerializer.Meta):
        model = FilmsGenres
        fields = AppOrgModelSerializer.Meta.fields + (
            "film",
            "genre",
        )


class GenresSerializer(DictionarySerializer):
    class Meta(DictionarySerializer.Meta):
        model = Genre
        read_only_fields = ("slug",)
        fields = DictionarySerializer.Meta.fields + read_only_fields
