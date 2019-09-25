from django.db import models
from clients.models import Client


class Invoice(models.Model):
    title = models.CharField(max_length=200)
    # user
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    body = models.TextField()
    invoice_total = models.DecimalField(max_digits=6, decimal_places=2)
    create_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.title

    def get_invoice_total(self):
        return f'${self.invoice_total}'
