from django.urls import path

from .views import (
    Auth0CallbackView,
    Auth0LoginView,
    DashboardView,
    MyLoginView,
    RegisterView,
)

urlpatterns = [
    path("login/", MyLoginView.as_view(), name="login"),
    path("login/auth0/", Auth0LoginView.as_view(), name="auth0_login"),
    path("callback/", Auth0CallbackView.as_view(), name="callback"),
    path("register/", RegisterView.as_view(), name="register"),
    path("dashboard/", DashboardView.as_view(), name="dashboard"),
]
