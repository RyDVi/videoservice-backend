from django.urls import path

from .views import CustomerAuthenticationView, CRMAuthenticationView, SignupCustomersViewSet, logout_user, accept_email, send_email_for_restore_password, set_new_password

def auth_url_patterns(base_router, lpath):
    return [
        path(lpath + "auth/login/", CustomerAuthenticationView.as_view()),
        path(lpath + "auth/signup/", SignupCustomersViewSet.as_view({'post': 'create'})),
        path(lpath + "auth/signup/accept_email/<uidb64>/<token>/", accept_email, name="accept_email"),
        path(lpath + "auth/restore_password/send_email_for_restore_password/", send_email_for_restore_password, name="send_email_for_restore_password"),
        path(lpath + "auth/restore_password/set_new_password/<uidb64>/<token>/", set_new_password, name="set_new_password"),
        path(lpath + "auth/staff/login/", CRMAuthenticationView.as_view()),
        path(lpath + "auth/logout/", logout_user, name="logout"),
        path(lpath + "auth/staff/logout/", logout_user, name="logout_staff"),
    ]
