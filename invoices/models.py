from decimal import Decimal
from django.db import models
from django.urls import reverse

from phonenumber_field.modelfields import PhoneNumberField



class Client(models.Model):
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    email = models.EmailField()
    company = models.CharField(max_length=100)
    address1 = models.CharField(max_length=100)
    address2 = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    phone_number = PhoneNumberField(blank=True)

    def get_absolute_url(self):
        return reverse('clien-detail', kwargs={'pk': self.pk})

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

    def __repr__(self):
        return f'Client: {self.first_name} {self.last_name}'
class Invoice(models.Model):
    title = models.CharField(max_length=200)
    # user
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    description = models.TextField()
    invoice_total = models.DecimalField(max_digits=6, decimal_places=2, blank=True, editable=False)
    create_date = models.DateField(auto_now_add=True)
    # line_item = models.ForeignKey(InvoiceItems, on_delete=models.CASCADE, blank=True)

    def get_absolute_url(self):
        return reverse('invoice-detail', kwargs={'pk': self.pk})

    def __str__(self):
        return self.title

    def __repr__(self):
        return f'<Invoice: {self.client} - {self.title}>'

    def get_invoice_total(self):
        # return f'${self.invoice_total}'
        total = Decimal('0.00')
        total = sum([item.subtotal() for item in self.items.all()])
        self.invoice_total = total

    def save(self, *args, **kwargs):
        self.get_invoice_total()
        super(Invoice, self).save(*args, **kwargs)

class InvoiceItems(models.Model):
    # Invoice Line Items
    invoice = models.ForeignKey(Invoice, related_name='items', on_delete=models.CASCADE)
    item = models.CharField(max_length=200)
    quantity = models.IntegerField(default=0)
    rate = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        # return self.item
        return f'{self.item} - {self.subtotal()}'

    def __repr__(self):
        return f'<Invoice Line Item: {self.item} - {self.subtotal()}>'

    def subtotal(self):
        return self.quantity * self.rate


