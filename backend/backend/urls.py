from django.contrib import admin
from django.urls import include, path
from rest_framework_nested import routers
from auth.urls import auth_url_patterns
from deals.urls import deals_url_patterns
from deals.views import DealTypesViewSet, DealsViewSet
from films.urls import film_url_patterns
from leads.urls import leads_url_patterns
from leads.views import LeadsViewSet
from organization.views import OrganizationViewSet
from users.urls import users_url_patterns
from users.views import (
    CustomersViewSet,
    UserMessagesViewSet,
    UsersViewSet,
)
from films.views import (
    CategoriesViewSet,
    FilmsCategoriesViewSet,
    FilmsGenresViewSet,
    FilmsPricesViewSet,
    FilmsPersonsViewSet,
    FilmsUsersViewSet,
    FilmsViewSet,
    GenresViewSet,
    PersonRolesViewSet,
    PersonsViewSet,
)
from django.conf import settings
from django.conf.urls.static import static
from videofiles.urls import video_url_patterns

from videofiles.views import SubtitleFileViewSet, VideoFileViewSet, VideoViewSet

api_v1_router = routers.DefaultRouter()
api_v1_router.register(r"users", UsersViewSet)
api_v1_router.register(r"films", FilmsViewSet)
api_v1_router.register(r"organizations", OrganizationViewSet)
api_v1_router.register(r"person_roles", PersonRolesViewSet)
api_v1_router.register(r"persons", PersonsViewSet)
api_v1_router.register(r"categories", CategoriesViewSet)
api_v1_router.register(r"films_users", FilmsUsersViewSet)
api_v1_router.register(r"films_persons", FilmsPersonsViewSet)
api_v1_router.register(r"films_categories", FilmsCategoriesViewSet)
api_v1_router.register(r"films_prices", FilmsPricesViewSet)
api_v1_router.register(r"deals", DealsViewSet)
api_v1_router.register(r"deal_types", DealTypesViewSet)
api_v1_router.register(r"customers", CustomersViewSet)
api_v1_router.register(r"leads", LeadsViewSet)
api_v1_router.register(r"video", VideoViewSet)
api_v1_router.register(r"videofiles", VideoFileViewSet)
api_v1_router.register(r"subtitlefiles", SubtitleFileViewSet)
api_v1_router.register(r"films_genres", FilmsGenresViewSet)
api_v1_router.register(r"genres", GenresViewSet)
api_v1_router.register(r"messages", UserMessagesViewSet)


API_URL = r"api/v1/"

api_v1_patterns = (
    [
        path(API_URL, include(api_v1_router.urls)),
    ]
    + film_url_patterns(api_v1_router, API_URL)
    + users_url_patterns(api_v1_router, API_URL)
    + deals_url_patterns(api_v1_router, API_URL)
    + leads_url_patterns(api_v1_router, API_URL)
    + auth_url_patterns(api_v1_router, API_URL)
    + video_url_patterns(api_v1_router, API_URL)
)


urlpatterns = (
    [
        path("admin/", admin.site.urls),
        path("api-auth/", include("rest_framework.urls", namespace="rest_framework")),
    ]
    + api_v1_patterns
)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
