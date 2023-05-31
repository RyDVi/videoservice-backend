from django.contrib.auth.models import User, AbstractUser
from django.db import models
from backend.models import BaseAppModel
from django.utils.translation import gettext_lazy as _

from organization.models import Organization
from .managers import UserMessagesQuerySet, CustomerQuerySet

# Делает поле email уникальным для класса User
User._meta.get_field("email")._unique = True


class Customer(User):
    org = models.ForeignKey(
        Organization,
        related_name="+",
        on_delete=models.CASCADE,
    )

    objects = CustomerQuerySet()


class UserMessage(BaseAppModel):
    sender = models.ForeignKey(
        User, related_name="sender_messages", on_delete=models.CASCADE
    )
    recipient = models.ForeignKey(
        User, related_name="recipient_messages", on_delete=models.CASCADE
    )
    text = models.TextField(verbose_name=_("text of message"))
    created_at = models.DateTimeField(verbose_name=_("datetime of creation"))

    objects = UserMessagesQuerySet.as_manager()
    
    class Meta:
        db_table = "user_messages"
