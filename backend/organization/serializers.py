from rest_framework import serializers

from organization.models import Organization


class OrganizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organization
        fields = ("id", "code", "name", "domain", "is_active", "cors")


