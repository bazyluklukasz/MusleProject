import uuid
from django.db import models


# Create your models here.


class Order(models.Model):
    class OrderType(models.TextChoices):
        WARDROBE_REVIEW = 'wardrobe_review', 'Przegląd Szafy'
        STYLING = 'styling', 'Stylizacja 1:1'
        CAPSULE = 'capsule', 'Szafa Kapsułowa'

    class Status(models.TextChoices):
        PENDING = 'pending', 'Oczekujące'
        ACTIVE = 'active', 'W realizacji'
        COMPLETED = 'completed', 'Zakończone'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    customer = models.ForeignKey('accounts.User', on_delete=models.CASCADE, related_name='customer_orders')

    type = models.CharField(
        max_length=50,
        choices=OrderType.choices,
        default=OrderType.WARDROBE_REVIEW,
    )
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING,
    )
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.get_type_display()} - {self.customer.username} ({self.get_status_display()})"
