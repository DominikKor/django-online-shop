from django import forms
from django.utils.translation import gettext_lazy as _

MAX_PRODUCTS = 20
PRODUCT_QUANTITY_CHOICES = [(i, str(i)) for i in range(1, MAX_PRODUCTS + 1)]


class CartAddProductForm(forms.Form):
    quantity = forms.TypedChoiceField(choices=PRODUCT_QUANTITY_CHOICES, coerce=int, label=_("quantity"))
    override_quantity = forms.BooleanField(required=False, initial=False, widget=forms.HiddenInput)
