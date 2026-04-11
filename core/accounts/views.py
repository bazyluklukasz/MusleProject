# Create your views here.
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView

from .forms import FormRegister


class MyLoginView(LoginView):
    template_name = "accounts/login.html"


class RegisterView(CreateView):
    form_class = FormRegister
    template_name = "accounts/register.html"
    success_url = reverse_lazy("login")


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = "accounts/dashboard.html"
