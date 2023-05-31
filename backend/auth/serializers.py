from django.utils.translation import gettext_lazy as _
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework import serializers
from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.password_validation import validate_password
from organization.base.serializers import AppOrgModelSerializer

from users.models import Customer

from .services import on_restore, on_signup


class BaseAuthSerializer(AuthTokenSerializer):
    def authenticate_user(self, username, password, **kwargs):
        return authenticate(
            request=self.context.get("request"),
            username=username,
            password=password,
            **kwargs
        )

    def validate(self, attrs):
        username = attrs.get("username")
        password = attrs.get("password")

        if username and password:
            user = self.authenticate_user(username, password)

            # The authenticate call simply returns None for is_active=False
            # users. (Assuming the default ModelBackend authentication
            # backend.)
            if not user:
                msg = _("Unable to log in with provided credentials.")
                raise serializers.ValidationError(msg, code="authorization")
        else:
            msg = _('Must include "username" and "password".')
            raise serializers.ValidationError(msg, code="authorization")

        attrs["user"] = user
        return attrs


class CRMAuthSerializer(BaseAuthSerializer):
    def authenticate_user(self, username, password):
        return super().authenticate_user(username, password, is_staff=True)


class CustomerAuthSerializer(BaseAuthSerializer):
    def authenticate_user(self, username, password):
        return super().authenticate_user(username, password, is_staff=False)


class SignupCustomerSerializer(AppOrgModelSerializer):
    password_repeat = serializers.CharField(write_only=True)

    class Meta(AppOrgModelSerializer.Meta):
        model = Customer
        fields = AppOrgModelSerializer.Meta.fields + (
            "username",
            "email",
            "password",
            "password_repeat",
        )
        extra_kwargs = {
            "password": {"write_only": True},
            "password_repeat": {"write_only": True},
        }

    def validate_password(self, value):
        validate_password(value)
        return value

    def validate(self, attrs):
        if attrs.get("password") != attrs.get("password_repeat"):
            raise serializers.ValidationError({"password": _("Passwords mismatch")})
        return super().validate(attrs)

    def create(self, validated_data):
        validated_data.pop("password_repeat")
        user = Customer.objects.create_user(**validated_data, is_active=False)

        on_signup(user)

        return user


class NewPasswordSerializer(serializers.Serializer):
    password = serializers.CharField()
    password_repeat = serializers.CharField()
    
    def validate_password(self, value):
        validate_password(value)
        return value

    def validate(self, attrs):
        if attrs.get("password_repeat") != attrs.get("password"):
            raise serializers.ValidationError(
                {"password_repeat": "Пароли не совпадают"}
            )
        return super().validate(attrs)
