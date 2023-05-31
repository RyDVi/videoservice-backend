from rest_framework import serializers

from backend.serializers import ChildListSerializer
from django.db import models


class CurrentOrgDefault:
    requires_context = True

    def __call__(self, serializer_field):
        return serializer_field.context["request"].org

    def __repr__(self):
        return "CurrentOrgDefault()"


class AppRelatedFieldMixin:
    def __init__(self, *args, **kwargs):
        if not kwargs.get("read_only"):
            assert "queryset" in kwargs
        super().__init__(*args, **kwargs)

    def get_queryset(self):
        model = self.queryset.model
        if hasattr(model, "tenant_link") or hasattr(model, "org"):
            request = self.context.get("request")
            if request:
                return self.queryset.filter(**{getattr(model, "tenant_link", "org"): request.org})
            return self.queryset.none()
        return super().get_queryset()


class AppPrimaryKeyRelatedField(
    AppRelatedFieldMixin, serializers.PrimaryKeyRelatedField
):
    def to_representation(self, value):
        if self.pk_field is not None:
            return str(self.pk_field.to_representation(value.pk))
        return str(value.pk)


class AppSlugRelatedField(AppRelatedFieldMixin, serializers.SlugRelatedField):
    pass


class AppModelSerializer(serializers.ModelSerializer):
    serializer_related_field = AppPrimaryKeyRelatedField
    serializer_related_to_field = AppSlugRelatedField
    serializer_field_mapping = {
        **serializers.ModelSerializer.serializer_field_mapping,
        models.AutoField: serializers.CharField,
        models.BigAutoField: serializers.CharField,
    }

    class Meta:
        read_only_fields = ("id", "url",)
        fields = read_only_fields
        list_serializer_class = ChildListSerializer


class AppOrgModelSerializer(AppModelSerializer):
    org = serializers.HiddenField(default=CurrentOrgDefault())

    class Meta(AppModelSerializer.Meta):
        read_only_fields = ("org",)
        fields = read_only_fields + AppModelSerializer.Meta.fields


class DictionarySerializer(AppOrgModelSerializer):
    class Meta(AppOrgModelSerializer.Meta):
        fields = AppOrgModelSerializer.Meta.fields + ("name",)
