from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView

from .models import Invoice, Client, InvoiceItems


class DashboardView(ListView):
    # TODO: Consider removing this or InvoiceListView
    model = Invoice
    template_name = 'dashboard.html'

class InvoiceListView(ListView):
    model = Invoice
    template_name = 'home.html'

class InvoiceDetailView(DetailView):
    model = Invoice
    template_name = 'invoice_detail.html'
    # invoice_items = Invoice.items.all()
    # https://stackoverflow.com/questions/12187751/django-pass-multiple-models-to-one-template

    def get_context_data(self, **kwargs):
        # print context
        # Call the base implementation first to get the data
        context = super(InvoiceDetailView, self).get_context_data(**kwargs)
        # Add client to the context -- to be used by invoice template
        client = context['invoice'].client
        context['client'] = client
        # Add invoice items queryset
        context['invoice_items'] = context['invoice'].items.all()
        return context

class InvoiceCreateView(CreateView):
    model = Invoice
    template_name = 'new_invoice.html'
    fields = '__all__'


class ClientCreateView(CreateView):
    model = Client
    template_name = 'new_client.html'
    fields = '__all__' # All fields on the form should be used


class ClientListView(ListView):
    model = Client
    template_name = 'clients.html'


class ClientDetailView(DetailView):
    model = Client
    template_name = 'client_detail.html'

class ClientUpdateView(UpdateView):
    pass
