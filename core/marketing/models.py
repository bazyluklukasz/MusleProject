import uuid

from django.db import models


class Discount_Code(models.Model):  # TODO DiscountCode rename.
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    partner_name = models.CharField(max_length=100)
    partner_category = models.CharField(max_length=100)
    code_string = models.CharField(max_length=100)
    discount_percentage = models.IntegerField(default=10)
    is_vip_only = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.partner_name} - {self.code_string}"
