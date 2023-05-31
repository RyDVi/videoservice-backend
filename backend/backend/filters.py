import base64
import binascii
import json
import re

import django_filters
from django import forms
from django.db.models import Q
from django_filters.fields import RangeField

PHONE_SUB = re.compile(r"[\-\(\)\s\+]+")


def is_looks_like_phone(value):
    value = re.sub(PHONE_SUB, "", value)
    return value.isdigit()


def reformat_phone_for_search(phone):
    phone = phone.strip()
    if phone.startswith("+1"):
        phone = phone[2:]
    phone = re.sub(PHONE_SUB, "", phone)
    result = "("
    for i, c in enumerate(phone):
        if i == 3:
            result += ") "
        elif i == 6:
            result += "-"
        result += c
    return result


def search_by_email(queryset, value, email_field):
    if email_field and "@" in value:
        return queryset.filter(**{email_field: value})


def search_by_phone(queryset, value, phone_field):
    if phone_field and is_looks_like_phone(value):
        return queryset.filter(**{phone_field: reformat_phone_for_search(value)})


def search_by_name(queryset, value, first_name_field, last_name_field):
    value = value.replace(",", "").split()
    lookup = None
    if len(value) == 1:
        token = value[0]
        lookup = Q(**{first_name_field: token}) | Q(**{last_name_field: token})
    elif len(value) == 2:
        token_1, token_2 = value
        lookup = (
            Q(**{first_name_field: token_1}) & Q(**{last_name_field: token_2})
        ) | (Q(**{first_name_field: token_2}) & Q(**{last_name_field: token_1}))
    else:
        for token in value:
            if not lookup:
                lookup = Q(**{last_name_field: token})
            else:
                lookup |= Q(**{last_name_field: token})
    return queryset.filter(lookup)


def search_by_fullname(queryset, value, first_name_field, last_name_field):
    value = value.replace(",", "").split()
    if len(value) == 2:
        token_1, token_2 = value
        lookup = (
            Q(**{first_name_field: token_1}) & Q(**{last_name_field: token_2})
        ) | (Q(**{first_name_field: token_2}) & Q(**{last_name_field: token_1}))
        return queryset.filter(lookup)
    return queryset.none()


def search_filter(
    queryset,
    value,
    email_field="email__istartswith",
    phone_field="phone__istartswith",
    first_name_field="first_name__istartswith",
    last_name_field="last_name__istartswith",
):
    qs = search_by_email(queryset, value, email_field)
    if qs:
        return qs
    qs = search_by_phone(queryset, value, phone_field)
    if qs:
        return qs
    return search_by_name(queryset, value, first_name_field, last_name_field)


class UUIDInFilter(django_filters.BaseInFilter, django_filters.UUIDFilter):
    pass


class CharInFilter(django_filters.BaseInFilter, django_filters.CharFilter):
    pass


class ChoiceInFilter(django_filters.BaseInFilter, django_filters.ChoiceFilter):
    pass


class IntegerInFilter(django_filters.BaseInFilter, django_filters.Filter):
    field_class = forms.IntegerField


class JsonBase64Field(forms.CharField):
    def to_python(self, value):
        value = super().to_python(value)
        if value != self.empty_value:
            try:
                return json.loads(base64.b64decode(value))
            except json.JSONDecodeError:
                raise forms.ValidationError("Invalid json.")
            except binascii.Error:
                raise forms.ValidationError("Invalid base64.")
        return value


class JsonFilter(django_filters.CharFilter):
    field_class = JsonBase64Field


class AgeRangeField(RangeField):
    def __init__(self, *args, **kwargs):
        super().__init__((forms.IntegerField(), forms.IntegerField()), *args, **kwargs)


class AgeRangeFilter(django_filters.RangeFilter):
    field_class = AgeRangeField
