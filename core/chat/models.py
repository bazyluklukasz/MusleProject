import uuid

from django.conf import settings
from django.db import models


class Message(models.Model):
    class Sender(models.TextChoices):
        CUSTOMER = "customer", "Customer"
        STYLIST = "stylist", "Stylist"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    customer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="customer_messages",
    )
    stylist = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="stylist_messages",
    )

    order = models.ForeignKey(
        "orders.Order", on_delete=models.CASCADE, related_name="messages"
    )

    sender_type = models.CharField(
        max_length=50, choices=Sender.choices, default=Sender.CUSTOMER
    )

    content = models.TextField(null=True, blank=True)

    attachment_url = models.URLField(max_length=500, null=True, blank=True)
    product_link = models.URLField(max_length=500, null=True, blank=True)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["created_at"]

    def __str__(self):
        return (
            f"Wiadomość w zleceniu {self.order_id} od {self.get_sender_type_display()}"
        )
