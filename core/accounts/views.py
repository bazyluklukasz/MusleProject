from urllib.parse import urlencode

import requests
from chat.models import Message
from django.conf import settings
from django.contrib.auth import get_user_model, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, PasswordResetView
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponse
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView, View
from marketing.models import Discount_Code

from .forms import UserRegisterForm

User = get_user_model()


class MyLoginView(LoginView):
    template_name = "accounts/login.html"


class Auth0LoginView(View):
    def get(self, request):
        params = {
            "response_type": "code",
            "client_id": settings.AUTH0_CLIENT_ID,
            "redirect_uri": settings.AUTH0_CALLBACK_URL,
            "scope": "openid profile email",
        }
        url = f"https://{settings.AUTH0_DOMAIN}/authorize?{urlencode(params)}"
        return redirect(url)


class Auth0CallbackView(View):
    def get(self, request):
        code = request.GET.get("code")
        error = request.GET.get("error")

        if error:
            return HttpResponse(f"Błąd z Auth0: {request.GET.get('error_description')}")

        if not code:
            return HttpResponse("Brak kodu. Spróbuj zalogować się ponownie.")

        token_url = f"https://{settings.AUTH0_DOMAIN}/oauth/token"
        token_data = {
            "grant_type": "authorization_code",
            "client_id": settings.AUTH0_CLIENT_ID,
            "client_secret": settings.AUTH0_CLIENT_SECRET,
            "code": code,
            "redirect_uri": settings.AUTH0_CALLBACK_URL,
        }

        response = requests.post(token_url, data=token_data)
        token_json = response.json()

        if "access_token" not in token_json:
            return HttpResponse(
                f"Serwer Auth0 odrzucił żądanie. Szczegóły: {token_json}"
            )

        user_info_url = f"https://{settings.AUTH0_DOMAIN}/userinfo"
        user_info = requests.get(
            user_info_url,
            headers={"Authorization": f"Bearer {token_json['access_token']}"},
        ).json()

        email = user_info.get("email")
        if not email:
            return HttpResponse(
                "Nie udało się pobrać emaila z konta Google. Spróbuj ponownie."
            )

        user, created = User.objects.get_or_create(
            username=email, defaults={"email": email}
        )

        login(request, user, backend="django.contrib.auth.backends.ModelBackend")
        return redirect("dashboard")


class RegisterView(CreateView):
    form_class = UserRegisterForm
    template_name = "accounts/register.html"
    success_url = reverse_lazy("login")


class ResetPassword(SuccessMessageMixin, PasswordResetView):
    template_name = "accounts/reset_password.html"
    email_template_name = "accounts/reset_password.html"
    success_url = reverse_lazy("login")


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = "accounts/dashboard.html"
    MAX_WARDROBE = 5

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user

        wardrobe_qs = user.wardrobe_items.all()
        wardrobe_count = wardrobe_qs.count()

        context.update(
            {
                "active_nav": "dashboard",
                "wardrobe_count": wardrobe_count,
                "last_wardrobe_item": wardrobe_qs.order_by("-added_at").first(),
                "wardrobe_fill_percent": self._get_wardrobe_fill(wardrobe_count),
                "discount_codes": self._get_discount_codes(user),
                "unread_messages_count": self._get_unread_count(user),
            }
        )
        return context

    def _get_wardrobe_fill(self, count):
        if self.MAX_WARDROBE == 0:
            return 0
        return min(int((count / self.MAX_WARDROBE) * 100), 100)

    def _get_discount_codes(self, user):
        if user.subscription_plan == "vip":
            return Discount_Code.objects.all()
        return Discount_Code.objects.filter(is_vip_only=False)

    def _get_unread_count(self, user):
        if user.subscription_plan == "vip":
            return Message.objects.filter(
                customer=user, is_read=False, sender_type="stylist"
            ).count()
        return 0
