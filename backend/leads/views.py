from backend.views import RelatedViewSetsMixin
from leads.models import Lead
from leads.serializers import LeadSerializer
from organization.base.views import AppModelViewSet


class LeadsViewSet(RelatedViewSetsMixin, AppModelViewSet):
    queryset = Lead.objects.all()
    serializer_class = LeadSerializer

    related_lookups = {"customer_pk": "customer"}
