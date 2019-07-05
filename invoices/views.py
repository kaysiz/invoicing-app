from django.shortcuts import render
from django.views.generic import ListView, DetailView

from .models import Invoice


class InvoiceListView(ListView):
    model = Invoice
    template_name = 'home.html'
