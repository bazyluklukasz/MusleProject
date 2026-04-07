import uuid

from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class User(AbstractUser):
    class Roles(models.TextChoices):
        USER = "user", "User"
        ADMIN = "admin", "Admin"
        STYLIST = "stylist", "Stylist"

    class SubPlan(models.TextChoices):
        BASE = "base", "Base"
        PREMIUM = "premium", "Premium"
        VIP = "vip", "VIP"

    role = models.CharField(
        max_length=20,
        choices=Roles.choices,
        default=Roles.USER,
    )

    subscription_plan = models.CharField(
        max_length=20,
        choices=SubPlan.choices,
        default=SubPlan.BASE,
    )

    used_stylist_reviews = models.IntegerField(default=0)
    max_stylist_reviews = models.IntegerField(default=5)


class UserProfile(models.Model):
    class Size(models.TextChoices):
        S32 = "32", "32"
        S34 = "34", "34"
        S36 = "36", "36"
        S38 = "38", "38"
        S40 = "40", "40"
        S42 = "42", "42"
        S44 = "44", "44"
        S46 = "46", "46"
        S48 = "48", "48"
        S50 = "50", "50"
        S52 = "52", "52"

    class Body(models.TextChoices):
        KLEPSYDRA = "klepsydra", "Klepsydra"
        GRUSZKA = "gruszka", "Gruszka"
        JABLKO = "jablko", "Jabłko"
        PROSTOKAT = "prostokat", "Prostokąt"
        ODWROCONY_TROJKAT = "odwrocony_trojkat", "Odwrócony Trójkąt"

    class BeautyType(models.TextChoices):
        JASNA_WIOSNA = "jasna_wiosna", "Jasna Wiosna"
        PRAWDZIWA_WIOSNA = "prawdziwa_wiosna", "Prawdziwa Wiosna"
        ZYWA_WIOSNA = "zywa_wiosna", "Żywa Wiosna"
        JASNE_LATO = "jasne_lato", "Jasne Lato"
        PRAWDZIWE_LATO = "prawdziwe_lato", "Prawdziwe Lato"
        MIEKKIE_LATO = "miekkie_lato", "Miękkie Lato"
        MIEKKA_JESIEN = "miekka_jesien", "Miękka Jesień"
        PRAWDZIWA_JESIEN = "prawdziwa_jesien", "Prawdziwa Jesień"
        GLEBOKA_JESIEN = "gleboka_jesien", "Głęboka Jesień"
        GLEBOKA_ZIMA = "gleboka_zima", "Głęboka Zima"
        PRAWDZIWA_ZIMA = "prawdziwa_zima", "Prawdziwa Zima"
        JASNA_ZIMA = "jasna_zima", "Jasna Zima"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    size = models.CharField(
        max_length=40,
        choices=Size.choices,
        default=Size.S32,
    )

    height = models.PositiveIntegerField(
        default=160,
        validators=[MinValueValidator(100), MaxValueValidator(220)],
    )
    body_type = models.CharField(
        max_length=40,
        choices=Body.choices,
        default=Body.KLEPSYDRA,
    )

    beauty_type = models.CharField(
        max_length=40,
        choices=BeautyType.choices,
        default=BeautyType.JASNE_LATO,
    )

    style_tag = models.CharField(
        max_length=200,
        null=True,
        blank=True,
    )
    favourite_brand = models.CharField(
        max_length=200,
        null=True,
        blank=True,
    )

    def __str__(self):
        return f"Profile {self.user.username} id = {self.id}"
