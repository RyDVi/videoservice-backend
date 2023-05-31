from django.db import models

from organization.base.models import AppOrgModel
from users.models import Customer


class DealType(AppOrgModel):
    """For example: rent, full buy of film"""

    name = models.CharField(max_length=255, default="")

    class Meta:
        db_table = "deal_types"
        constraints = [
            models.UniqueConstraint(
                fields=["name", "org"], name="unique by org and type name"
            )
        ]


class Deal(AppOrgModel):
    price = models.DecimalField(decimal_places=2, max_digits=20)
    type = models.ForeignKey(DealType, null=False, blank=False, related_name="deal", on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, null=False, blank=False, related_name="deal", on_delete=models.CASCADE)

    class Meta:
        db_table = "deals"
