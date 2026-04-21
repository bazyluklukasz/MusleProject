from django import forms

from .models import WardrobeItem


class WardrobeForm(forms.ModelForm):
    class Meta:
        model = WardrobeItem
        fields = ("name", "category", "brand", "size", "image_url")
        widgets = {
            "name": forms.TextInput(attrs={"placeholder": "np. Czarna spódnica midi"}),
            "brand": forms.TextInput(attrs={"placeholder": "np. Zara, Reserved..."}),
            "size": forms.TextInput(attrs={"placeholder": "np. M, 38, S"}),
            "image_url": forms.URLInput(attrs={"placeholder": "https://..."}),
        }
