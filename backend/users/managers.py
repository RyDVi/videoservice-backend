from organization.base.models import OrgQuerySet
from django.db.models import Q
from django.contrib.auth.models import UserManager

class UserMessagesQuerySet(OrgQuerySet):
    def for_user(self, user_id):
        return self.filter(Q(sender=user_id)|Q(recipient=user_id))
    
    
class CustomerQuerySet(UserManager):
    def for_email_or_username(self, email_or_username):
        return self.filter(Q(email=email_or_username)|Q(username=email_or_username), is_staff=False, is_superuser=False)