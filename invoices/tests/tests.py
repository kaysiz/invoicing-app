from django.test import TestCase
from django.urls import reverse

from invoices.models import Invoice, Client


class InvoiceTests(TestCase):

    def setUp(self):
        # create sample Invoice and Client
        Client.objects.create(first_name="Test", last_name="Client", email="test@example.com", company="Xcorp")
        Invoice.objects.create(title="Test Invoice 1", client=Client.objects.get(id=1), body="Test  1", invoice_total=200)


    def test_invoice_object_content(self):
        invoice = Invoice.objects.get(id=1)
        expected_invoice_title = f'{invoice.title}'
        self.assertEqual(expected_invoice_title, "Test Invoice 1")

    def test_invoice_str_method(self):
        invoice = Invoice.objects.get(id=1)
        expected_invoice_str = str(invoice)
        self.assertEqual(expected_invoice_str, "Test Invoice 1")

    def test_invoice_repr_method(self):
        invoice = Invoice.objects.get(id=1)
        expected_invoice_repr = repr(invoice)
        self.assertEqual(expected_invoice_repr, "<Invoice: Test Client - Test Invoice 1>")


class ClientTests(TestCase):

    def setUp(self):
        # create sample Invoice and Client
        Client.objects.create(first_name="Test", last_name="Client", email="test@example.com", company="Xcorp")

    def test_client_object_content(self):
        client = Client.objects.get(id=1)
        expected_first_name = f'{client.first_name}'
        self.assertEqual(expected_first_name, "Test")

    def test_client_object_repr(self):
        client = Client.objects.get(id=1)
        self.assertEqual(repr(client), "Client: Test Client")

    def test_client_str(self):
        client = Client.objects.get(id=1)
        self.assertEqual(str(client), "Test Client")


class ViewsTests(TestCase):

    def test_dashboard_view(self):
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Invoicing App")
        self.assertTemplateUsed(response, 'dashboard.html')

    def test_add_client_view(self):
        response = self.client.get(reverse('new-client'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'new_client.html')
