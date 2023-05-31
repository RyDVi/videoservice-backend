from django.utils.translation import gettext_lazy as _
from django.core.mail import send_mail
from .tokens import account_activation_token, restore_password_token

from django.utils.encoding import force_bytes 
from django.utils.http import urlsafe_base64_encode 
from django.template.loader import render_to_string 


def on_signup(user):
    message = render_to_string(
        "acc_active_email_ru.html",
        {
            "user": user,
            "domain": user.org.domain,
            "uid": urlsafe_base64_encode(force_bytes(user.pk)),
            "token": account_activation_token.make_token(user),
        },
    )
    send_mail(
        # _("Confirmation of registration"),
        "Подтверждение регистрации",
        # Для подтверждения регистрации на сайте перейдите по следующей ссылке:
        message,
        "from@example.com",
        [user.email],
    )


def on_restore(user):
    message = render_to_string(
        "restore_password_ru.html",
        {
            "user": user,
            "domain": user.org.domain,
            "uid": urlsafe_base64_encode(force_bytes(user.pk)),
            "token": restore_password_token.make_token(user),
        },
    )
    send_mail(
        # _("Confirmation of registration"),
        "Восстановление пароля",
        # Для подтверждения регистрации на сайте перейдите по следующей ссылке:
        message,
        "from@example.com",
        [user.email],
    )