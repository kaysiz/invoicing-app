from django.db import models

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

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

    def __repr__(self):
        return f'Client: {self.first_name} {self.last_name}'


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
