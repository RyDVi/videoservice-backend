import json
from django.http import HttpResponse
from openai import Customer
from auth.services import on_restore

from organization.base.views import AppGenericViewSet
from .serializers import (
    CRMAuthSerializer,
    CustomerAuthSerializer,
    NewPasswordSerializer,
)
from rest_framework.response import Response

from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from django.contrib.auth import logout
from rest_framework import mixins
from rest_framework.permissions import AllowAny
from .serializers import SignupCustomerSerializer
from .tokens import account_activation_token
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_str
from users.models import Customer
from rest_framework.decorators import api_view, permission_classes


class BaseAuthenticationView(ObtainAuthToken):
    def get_response_user_data(self, token, user):
        return {"token": token.key, "user_id": user.pk, "email": user.email}

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        token, created = Token.objects.get_or_create(user=user)
        return Response(self.get_response_user_data(token, user))


def build_auth_data(user, token):
    return {"token": token.key, "user_id": user.pk, "email": user.email}


class CRMAuthenticationView(BaseAuthenticationView):
    serializer_class = CRMAuthSerializer

    def get_response_user_data(self, token, user):
        return build_auth_data(user, token)


class CustomerAuthenticationView(BaseAuthenticationView):
    serializer_class = CustomerAuthSerializer

    def get_response_user_data(self, token, user):
        return build_auth_data(user, token)


def logout_user(request):
    logout(request)
    return HttpResponse()


class SignupCustomersViewSet(mixins.CreateModelMixin, AppGenericViewSet):
    permission_classes = [AllowAny]
    serializer_class = SignupCustomerSerializer


def accept_email(request, uidb64, token):
    User = Customer
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        if user.is_active:
            return HttpResponse(
                json.dumps(
                    {
                        "non_field_errors": [
                            "Почта уже подтверждена. Авторизуйтесь на сайте с помощью лоигина/почты и пароля."
                        ]
                    }
                ),
                status=400,
            )
        user.is_active = True
        user.save()
        token, created = Token.objects.get_or_create(user=user)
        return HttpResponse(json.dumps(build_auth_data(user, token)), status=200)
    else:
        return HttpResponse(
            json.dumps(
                {"non_field_errors": ["Токен или пользователь недействительны."]}
            ),
            status=400,
        )


@api_view(["POST"])
@permission_classes([AllowAny])
def send_email_for_restore_password(request):
    email_or_username = request.data.get("email_or_username")
    if not email_or_username:
        return HttpResponse(
            json.dumps({"email_or_username": "Предоставьте Email или логин"}),
            status=400,
        )
    users = Customer.objects.for_email_or_username(email_or_username)

    if not len(users):
        return HttpResponse(
            json.dumps(
                {"email_or_username": "Пользователь с такими данными не найден"}
            ),
            status=400,
        )
    on_restore(users.first())
    return HttpResponse(status=200)


@api_view(["POST"])
@permission_classes([AllowAny])
def set_new_password(request, uidb64, token):
    s = NewPasswordSerializer(data=request.data)
    s.is_valid(raise_exception=True)
    new_password = s.data.get('password')
    User = Customer
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.set_password(new_password)
        user.save()
        return HttpResponse(status=200)
    else:
        return HttpResponse(
            json.dumps(
                {"non_field_errors": ["Токен или пользователь недействительны."]}
            ),
            status=400,
        )
