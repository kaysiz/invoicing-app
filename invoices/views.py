from django.shortcuts import render
from django.views.generic import ListView, DetailView


class InvoiceListView(ListView):
    model = ''
    template_name = ''
