from django.conf import settings
from django.db import models
from django.http.request import split_domain_port
from django.utils.translation import gettext_lazy as _


class OrganizationManager(models.Manager):
    def get_current(self, request):
        host = request.get_host()
        return self.get_current_from_host(host)

    def get_current_from_host(self, host):
        if settings.DEBUG:
            if host.startswith("localhost:") or host.startswith("127.0.0.1:"):
                host = "localhost"
        try:
            return self.get(domain__iexact=host, is_active=True)
        except Organization.DoesNotExist:
            domain = split_domain_port(host)[0]
            return self.get(domain__iexact=domain, is_active=True)

    def get_by_natural_key(self, domain):
        return self.get(domain=domain)

    def active(self):
        return self.filters(is_active=True)


class Organization(models.Model):
    id = models.AutoField(_("id"), primary_key=True)
    name = models.CharField(_("name"), max_length=50, unique=True)
    code = models.CharField(_("code"), max_length=32, unique=True)
    domain = models.CharField(_("domain"), max_length=50, unique=True)
    is_active = models.BooleanField(_("is active"), default=True)
    cors = models.JSONField(_("allowed urls"), default=list)

    objects = OrganizationManager()

    class Meta:
        db_table = "organizations"
        constraints = [
            models.UniqueConstraint(fields=["code"], name="unique appversion")
        ]
