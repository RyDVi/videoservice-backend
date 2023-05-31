from leads.models import Lead
from organization.base.serializers import AppOrgModelSerializer


class LeadSerializer(AppOrgModelSerializer):
    class Meta(AppOrgModelSerializer.Meta):
        model = Lead
        fields = AppOrgModelSerializer.Meta.fields + ("customer",)
