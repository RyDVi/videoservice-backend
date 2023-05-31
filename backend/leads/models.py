from django.db import models

from organization.base.models import AppOrgModel
from users.models import Customer


class Lead(AppOrgModel):
    customer = models.OneToOneField(
        Customer, related_name="lead", on_delete=models.CASCADE
    )
    
    class Meta:
        db_table = 'leads'
