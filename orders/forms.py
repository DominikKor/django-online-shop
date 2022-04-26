from django import forms
from django.utils.translation import gettext_lazy as _
from localflavor.de.forms import DEZipCodeField

from .models import Order


class OrderCreateForm(forms.ModelForm):
    postal_code = DEZipCodeField(error_messages={'invalid': _("Please enter a valid German postal code.")})

    class Meta:
        model = Order
        fields = ["first_name", "last_name", "email", "address", "postal_code", "city"]
