from django.db import models
from backend.models import BaseAppModel
from django.utils.translation import gettext_lazy as _
from backend.utils import slugify
from organization.models import Organization


class OrgQuerySet(models.QuerySet):
    def from_org(self, org):
        if self.model.tenant_link or self.model.org:
            return self.filter(**{self.model.tenant_link or self.model.org: org})
        return self.none()


OrgManager = models.Manager.from_queryset(OrgQuerySet)


class BaseOrgModel(models.Model):
    org = models.ForeignKey(
        Organization,
        verbose_name=_("data of organization"),
        related_name="+",
        on_delete=models.CASCADE,
    )
    objects = OrgManager()

    class Meta:
        abstract = True


class AppOrgModel(BaseOrgModel, BaseAppModel):
    class Meta:
        abstract = True


class SlugFieldMixin(models.Model):
    slug = models.SlugField(_("slug"), max_length=256)

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        return super().save(*args, **kwargs)
