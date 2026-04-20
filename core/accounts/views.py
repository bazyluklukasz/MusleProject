# Create your views here.
from chat.models import Message
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, PasswordResetView
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView
from marketing.models import Discount_Code

from .forms import UserRegisterForm


class MyLoginView(LoginView):
    template_name = "accounts/login.html"


class RegisterView(CreateView):
    form_class = UserRegisterForm
    template_name = "accounts/register.html"
    success_url = reverse_lazy("login")


class ResetPassword(SuccessMessageMixin, PasswordResetView):
    template_name = "accounts/reset_password.html"
    email_template_name = "accounts/reset_password.html"

    success_url = reverse_lazy("accounts/login")


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
        percent = int((count / self.MAX_WARDROBE) * 100)
        return min(percent, 100)

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
