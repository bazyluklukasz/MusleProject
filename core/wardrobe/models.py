import uuid

from django.conf import settings
from django.db import models


class WardrobeItem(models.Model):
    # Kategorie ubrań widoczne na frontendzie
    class Category(models.TextChoices):
        TOP = "top", "Góra"
        BOTTOM = "bottom", "Dół"
        DRESS = "dress", "Sukienki"
        SHOES_ACC = "shoes_acc", "Buty i Dodatki"

    # Zastosowano UUID dla spójności z resztą systemu
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    # Bezpieczne odwołanie do głównego modelu User
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="wardrobe_items",
    )

    # Opcjonalna nazwa ubrania (np. "Czarna spódnica midi")
    name = models.CharField(max_length=255, null=True, blank=True)

    # Kategoria - niezbędna do filtrowania
    category = models.CharField(
        max_length=20, choices=Category.choices, default=Category.TOP
    )

    brand = models.CharField(max_length=255, null=True, blank=True)
    size = models.CharField(max_length=50, null=True, blank=True)

    # Jeśli trzymasz linki z zewnątrz użyj URLField.
    # Jeśli użytkownicy będą wgrywać piki (np. z dysku/telefonu) zmień to w przyszłości na:
    # image = models.ImageField(upload_to='wardrobe_images/', null=True, blank=True)
    image_url = models.URLField(max_length=500, null=True, blank=True)

    added_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.get_category_display()} - {self.brand or 'Brak marki'} ({self.user.username})"
