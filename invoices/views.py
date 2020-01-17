from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse, reverse_lazy
from django.forms.models import inlineformset_factory
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from .models import Invoice, Client, InvoiceItem
from .forms import InvoiceCreateForm

InvoiceItemsFormset = inlineformset_factory(
    Invoice, InvoiceItem, fields=('item', 'quantity', 'rate',),
    extra=1,
)


class InvoiceListView(LoginRequiredMixin, ListView):
    # model = Invoice --> This the same as Invoice.objects.all()

    template_name = 'dashboard.html'

    # Limit queryset to invoices by logged in user
    def get_queryset(self):
        if self.request.user.is_authenticated:
            return Invoice.objects.filter(user=self.request.user)
        else:
            return Invoice.objects.none()

class InvoiceDetailView(LoginRequiredMixin, DetailView):

    template_name = 'invoice_detail.html'


    def get_queryset(self):
        if self.request.user.is_authenticated:
            return Invoice.objects.filter(user=self.request.user)
        else:
            return Invoice.objects.none()

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get the data
        context = super(InvoiceDetailView, self).get_context_data(**kwargs)
        # Add client to the context -- to be used by invoice template
        client = context['invoice'].client
        context['client'] = client
        # Add invoice items queryset
        context['invoice_items'] = context['invoice'].items.all()
        user = context['invoice'].user
        context['user'] = user
        return context

class InvoiceCreateView(LoginRequiredMixin, CreateView):
    model = Invoice
    template_name = 'new_invoice.html'
    form_class = InvoiceCreateForm

    def get_form_kwargs(self):
        # The queryset for this view was created in the form
        # get_queryset() isn't used in create views
        kwargs = super(InvoiceCreateView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def get_context_data(self, **kwargs):
        # To display the invoice items
        # Call the base implementation first to get the data
        # context = super(InvoiceCreateView, self).get_context_data(**kwargs)
        # Add invoice items queryset
        data = super().get_context_data(**kwargs)
        if self.request.POST:
            data['invoice_items'] = InvoiceItemsFormset(self.request.POST)
        else:
            data['invoice_items'] = InvoiceItemsFormset()
        return data

    def form_valid(self, form):
        form.instance.user = self.request.user
        context = self.get_context_data()
        invoice_items = context['invoice_items']
        self.invoice = form.save()
        if invoice_items.is_valid():
            invoice_items.instance = self.invoice
            invoice_items.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('invoice-list')


class InvoiceUpdateView(LoginRequiredMixin, UpdateView):
    fields = ['title']
    template_name = 'edit_invoice.html'

    # Limit queryset to invoices created by logged in user
    def get_queryset(self):
        if self.request.user.is_authenticated:
            return Invoice.objects.filter(user=self.request.user)
        else:
            return Invoice.objects.none()

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        if self.request.POST:
            data['invoice_items'] = InvoiceItemsFormset(self.request.POST, instance=self.object)
        else:
            data['invoice_items'] = InvoiceItemsFormset(instance=self.object)
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        invoice_items = context['invoice_items']
        self.object = form.save()
        if invoice_items.is_valid():
            invoice_items.instance = self.object
            invoice_items.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('invoice-list')

class InvoiceDeleteView(LoginRequiredMixin, DeleteView):

    template_name = 'confirm_delete_invoice.html'
    success_url = reverse_lazy('invoice-list')

    # Limit queryset to invoices created by logged in user
    def get_queryset(self):
        if self.request.user.is_authenticated:
            return Invoice.objects.filter(user=self.request.user)
        else:
            return Invoice.objects.none()


class ClientCreateView(LoginRequiredMixin, CreateView):
    model = Client
    template_name = 'new_client.html'
    fields = (
                'first_name', 'last_name', 'email', 'company',
                'address1', 'address2', 'country', 'phone_number'
    )

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)


class ClientListView(LoginRequiredMixin, ListView):
    model = Client
    template_name = 'clients.html'


class ClientDetailView(LoginRequiredMixin, DetailView):
    template_name = 'client_detail.html'

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return Client.objects.filter(created_by=self.request.user)
        else:
            return Client.objects.none()

class ClientUpdateView(LoginRequiredMixin, UpdateView):
    template_name = 'edit_client.html'
    fields = [
        'first_name', 'last_name', 'email', 'company',
        'address1', 'address2', 'country', 'phone_number',
    ]


    def get_queryset(self):
        if self.request.user.is_authenticated:
            return Client.objects.filter(created_by=self.request.user)
        else:
            return Client.objects.none()
