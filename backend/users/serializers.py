from django.contrib.auth.models import User

from organization.base.serializers import AppModelSerializer, AppOrgModelSerializer
from users.models import Customer, UserMessage


class UserSerializer(AppOrgModelSerializer):
    class Meta:
        model = User
        fields = ["url", "username", "email", "is_staff"]
        extra_kwargs = {"password": {"write_only": True}}


class CustomerSerializer(AppOrgModelSerializer):
    class Meta(AppOrgModelSerializer.Meta):
        model = Customer
        fields = AppOrgModelSerializer.Meta.fields + (
            "username",
            "email",
            "first_name",
            "last_name",
        )

class UserMessagesSerializer(AppModelSerializer):
    class Meta(AppModelSerializer.Meta):
        model = UserMessage
        fields = AppModelSerializer.Meta.fields + (
            "sender",
            "recipient",
            "text",
            "created_at",
        )