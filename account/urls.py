#account/urls.py

from django.contrib.auth import views as auth_views
from django.urls import path

from .views import PasswordResetView, ProfileUpdateView, MyLoginView

app_name = "account"

urlpatterns = [
    path("login/", MyLoginView.as_view(), name="login"),
    # password change urls
    path(
        "profile/password-change/",
        auth_views.PasswordChangeView.as_view(),
        name="password_change",
    ),
    path(
        "profile/password-change/done/",
        auth_views.PasswordChangeDoneView.as_view(),
        name="password_change_done",
    ),
    # password reset urls
    path("password-reset/", PasswordResetView.as_view(), name="password_reset"),
    path(
        "password-reset/done/",
        auth_views.PasswordResetDoneView.as_view(),
        name="password_reset_done",
    ),
    path(
        "password-reset/<uidb64>/<token>/",
        auth_views.PasswordResetConfirmView.as_view(),
        name="password_reset_confirm",
    ),
    path(
        "password-reset/complete/",
        auth_views.PasswordResetCompleteView.as_view(),
        name="password_reset_complete",
    ),
    # profile urls
    path("profile/", ProfileUpdateView.as_view(), name="profile"),
    # path('profile/request-app-modification/', request_app_modification, name='request_app_modification'),
]