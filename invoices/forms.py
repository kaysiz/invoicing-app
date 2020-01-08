from django.forms import ModelForm
from .models import Invoice, InvoiceItem


class InvoiceItemsForm(ModelForm):
    class Meta:
        model = InvoiceItem
        fields = '__all__'
