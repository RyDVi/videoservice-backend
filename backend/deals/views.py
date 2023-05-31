from backend.views import RelatedViewSetsMixin
from deals.models import Deal, DealType
from deals.serializers import DealSerializer, DealTypeSerializer
from organization.base.views import AppModelViewSet


class DealTypesViewSet(RelatedViewSetsMixin, AppModelViewSet):
    queryset = DealType.objects.all()
    serializer_class = DealTypeSerializer

    related_lookups = {"deal_pk": "deal"}


class DealsViewSet(RelatedViewSetsMixin, AppModelViewSet):
    queryset = Deal.objects.all()
    serializer_class = DealSerializer

    related_lookups = {"deal_type_pk": "deal_type"}
