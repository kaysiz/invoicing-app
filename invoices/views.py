from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse, reverse_lazy
from django.forms import formset_factory, modelformset_factory
from django.forms.models import inlineformset_factory
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from .models import Invoice, Client, InvoiceItem
from .forms import InvoiceItemsForm

InvoiceItemsFormset = inlineformset_factory(
    Invoice, InvoiceItem, fields=('item', 'quantity', 'rate',),
    extra=1,
)


class InvoiceListView(LoginRequiredMixin, ListView):
    # model = Invoice --> Thi is the same as Invoice.objects.all()

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
    fields = ('title', 'client')

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return Client.objects.filter(created_by=self.request.user)
        else:
            return Client.objects.none()

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
        # TODO: Add a client queryset here Only allow user to select clients linked to them
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



# def invoice_create_view(request):
#     # https://docs.djangoproject.com/en/dev/topics/forms/modelforms/#inline-formsets
#     # https://github.com/elo80ka/django-dynamic-formset
#     # https://collingrady.wordpress.com/2008/02/18/editing-multiple-objects-in-django-with-newforms/
#     # https://stackoverflow.com/questions/18413303/how-can-i-have-the-equivalent-of-djangos-admin-inlines-in-a-modelform
#     # testFormSet = modelformset_factory(InvoiceItems, form=InvoiceItemsForm, fields=('invoice','item', 'quantity'), extra=0)
#     # formset = testFormSet()
#     # context = {
#     #     'formset': formset,
#     # }
#     if request.method == 'POST':
#         InvoiceItemsFormset = inlineformset_factory(
#             Invoice, InvoiceItems, fields=('item', 'quantity', 'rate', 'tax')
#         )
#         invoice = Invoice(request.POST)
#         formset = InvoiceItemsFormset(request.POST)
#         if invoice.is_valid() and formset.is_valid():
#             invoice_instance = invoice.save()
#             invoice_items = formset.save(commit=False)
#             for invoice_item in invoice_items:
#                 invoice_item.invoice_id = invoice_instance.id
#                 invoice_item.save()
#             invoice.save()
#             formset = InvoiceItemsFormset(queryset=InvoiceItems.objects.filter(invoice__id=invoice.pk))
#     else:
#         invoice = Invoice()
#         # invoice.save()
#         InvoiceItemsFormset = inlineformset_factory(
#             Invoice, InvoiceItems, fields=('invoice','item', 'quantity', 'rate', 'tax')
#         )
#         formset = InvoiceItemsFormset()



#     context ={
#         'formset': formset,
#         # 'form': invoice,
#     }
#     return render(request,'new_invoice_test.html', context)

# def edit_invoice(request, invoice_id):
#     # https://github.com/elo80ka/django-dynamic-formset
#     # https://simpleit.rocks/python/django/dynamic-add-form-with-add-button-in-django-modelformset-template/
#     # https://medium.com/all-about-django/adding-forms-dynamically-to-a-django-formset-375f1090c2b0
#     invoice = Invoice.objects.get(pk=invoice_id)
#     InvoiceItemsFormset = modelformset_factory(InvoiceItem, fields=('item', 'quantity','rate','tax',))
#
#     if request.method == 'POST':
#         formset = InvoiceItemsFormset(request.POST, queryset=InvoiceItem.objects.filter(invoice__id=invoice.pk))
#         if formset.is_valid():
#             instances = formset.save(commit=False)
#             for instance in  instances:
#                 instance.invoice_id = invoice.id
#                 instance.save()
#             invoice.save() # Do this in order to update invoice total
#     # else:
#     #     # Create a new invoice here
#     #     # https://docs.djangoproject.com/en/3.0/topics/forms/modelforms/#saving-objects-in-the-formset
#     #     formset = InvoiceItemsFormset(request.POST)
#     #     invoice = Invoice()
#     #     if formset.is_valid():
#     #         instances = formset.save(commit=False)
#
#
#     formset = InvoiceItemsFormset(queryset=InvoiceItem.objects.filter(invoice__id=invoice.pk))
#     return render(request, 'index.html', {'formset' : formset})
