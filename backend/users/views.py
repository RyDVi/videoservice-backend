from django.contrib.auth.models import User
from rest_framework.permissions import IsAdminUser
from backend.views import (
    FilterBackend,
    OrderingFilter,
    RelatedViewSetsMixin,
    StandardPagination,
)
from organization.base.views import AppModelViewSet
from .models import Customer, UserMessage

from .serializers import (
    CustomerSerializer,
    UserMessagesSerializer,
    UserSerializer,
)


class UsersViewSet(RelatedViewSetsMixin, AppModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]

    related_lookups = {"film_pk": "films", "films_users_pk": "films_users"}


class CustomersViewSet(RelatedViewSetsMixin, AppModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer

    related_lookups = {"lead_pk": "lead"}


class UserMessagesViewSet(RelatedViewSetsMixin, AppModelViewSet):
    queryset = UserMessage.objects.all()
    serializer_class = UserMessagesSerializer
    pagination_class = StandardPagination
    filter_backends = (
        FilterBackend,
        OrderingFilter,
    )
    ordering_fields = "__all__"
    
    def get_queryset(self):
        user_id = self.request.user.id
        if not user_id:
            return super().get_queryset().none()
        return super().get_queryset().for_user(user_id)
    
