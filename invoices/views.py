from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse, reverse_lazy
from django.forms.models import inlineformset_factory
from django.views.generic import View, ListView, DetailView, CreateView, UpdateView, DeleteView

from .models import Invoice, Client, InvoiceItem
from .forms import InvoiceCreateForm

from weasyprint import HTML


InvoiceItemsFormset = inlineformset_factory(
    Invoice, InvoiceItem, fields=('item', 'quantity', 'rate',),
    extra=1,
)


class HomePage(LoginRequiredMixin, ListView):
    template_name = 'home.html'
    context_object_name = 'invoices'

    def get_queryset(self):
        if self.request.user.is_authenticated:
            # Ensure queryset is cached
            invoices = Invoice.objects.filter(user=self.request.user)
            return invoices
        else:
            return Invoice.objects.none()

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get the data
        context = super(HomePage, self).get_context_data(**kwargs)
        try:
            recent_invoices = context['invoices'].order_by('-id')[:4]
        except (IndexError, AttributeError):
            recent_invoices = None
        context['recent_invoices'] = recent_invoices
        return context




class InvoiceListView(LoginRequiredMixin, ListView):
    # model = Invoice --> This the same as Invoice.objects.all()

    template_name = 'dashboard.html'

    def get_queryset(self):
        if self.request.user.is_authenticated:
            # Ensure queryset is cached
            invoices = Invoice.objects.filter(user=self.request.user)
            return invoices
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
    template_name = 'clients.html'

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return Client.objects.filter(created_by=self.request.user)
        else:
            return Client.objects.none()


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


@login_required
def generate_pdf_invoice(request, invoice_id):
    """Generate PDF Invoice"""

    queryset = Invoice.objects.filter(user=request.user)
    invoice = get_object_or_404(queryset, pk=invoice_id)

    client = invoice.client
    user = invoice.user
    invoice_items = InvoiceItem.objects.filter(invoice=invoice)


    context = {
        "invoice": invoice,
        "client": client,
        "user": user,
        "invoice_items": invoice_items,
    }

    html_template = render_to_string('pdf/html-invoice.html', context)

    pdf_file = HTML(string=html_template, base_url=request.build_absolute_uri()).write_pdf()
    pdf_filename = f'invoice_{invoice.id}.pdf'
    response = HttpResponse(pdf_file,
                            content_type='application/pdf')
    response['Content-Disposition'] = 'filename=%s' % (pdf_filename)
    return  response

    # invoice = Invoice.objects.get(id=3)
    # html_string = render_to_string('pdf/html-invoice.html', {'invoice': invoice})
    # html = HTML(string=html_string)
    # result = html.write_pdf()
    #
    # # Create HTTP Response
    # response = HttpResponse(content_type='application/pdf;')
    # response['Content-Disposition'] = 'inline; filename=invoice.pdf'
    # response['Content-Transfer-Encoding'] = 'binary'
    # with tempfile.NamedTemporaryFile(delete=True) as output:
    #     output.write(result)
    #     output.flush()
    #     output = open(output.name, 'r')
    #     response.write(output.read())
    # return response
