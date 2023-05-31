from re import A
from deals.models import Deal, DealType
from organization.base.serializers import AppOrgModelSerializer, DictionarySerializer


class DealTypeSerializer(DictionarySerializer):
    class Meta(DictionarySerializer.Meta):
        model = DealType
        fields = DictionarySerializer.Meta.fields


class DealSerializer(AppOrgModelSerializer):
    class Meta(AppOrgModelSerializer.Meta):
        model = Deal
        fields = AppOrgModelSerializer.Meta.fields + (
            "price",
            "type",
            "customer",
        )
