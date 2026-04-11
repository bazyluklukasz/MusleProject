from django.urls import path

from .views import DashboardView, MyLoginView, RegisterView

urlpatterns = [
    path("login/", MyLoginView.as_view(), name="login"),
    path("register/", RegisterView.as_view(), name="register"),
    path("dashboard/", DashboardView.as_view(), name="dashboard"),
]
