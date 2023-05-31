from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser

from organization.models import Organization
from organization.serializers import OrganizationSerializer

class OrganizationViewSet(viewsets.ModelViewSet):
    queryset = Organization.objects.all()
    serializer_class = OrganizationSerializer
    permission_classes = [IsAdminUser]
    