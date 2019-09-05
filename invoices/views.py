from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView

from .models import Invoice


class InvoiceListView(ListView):
    model = Invoice
    template_name = 'home.html'

class InvoiceCreateView(CreateView):
    model = Invoice
    template_name = 'new_invoice.html'
    fields = '__all__'

class DashboardView(ListView):
    model = Invoice
    template_name = 'dashboard.html'
