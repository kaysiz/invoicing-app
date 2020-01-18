import datetime

from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model, authenticate, login

from invoices.models import Invoice, InvoiceItem, Client


class InvoiceTests(TestCase):

    def setUp(self):
        # create sample Invoice, Client, and User
        self.user = get_user_model().objects.create_user(
            username='testuser',
            email='test@email.com',
            password='secretpassword'
        )

        self.client1 = Client.objects.create(
            first_name="Test", last_name="Client", email="test@example.com",
            company="Xcorp", address1="1234 Paradise Lane",
            address2="Good Street", country="Zimbabwe",
            phone_number="+263772873063",
            created_by=self.user
        )

        self.invoice = Invoice.objects.create(
            title="Test Invoice 1",
            user=self.user,
            client=self.client1,
            create_date=datetime.datetime.now()
        )

        self.invoice_item1 = InvoiceItem.objects.create(
            invoice=self.invoice,
            item="Test Line Item",
            quantity=3,
            rate=20,
            tax=0,
        )

        self.invoice_item2 = InvoiceItem.objects.create(
            invoice=self.invoice,
            item="Test Line Item 2",
            quantity=1,
            rate=20,
            tax=0,
        )
        self.invoice.save()

    def test_invoice_object_content(self):
        invoice = Invoice.objects.get(id=1)
        expected_invoice_title = f'{invoice.title}'
        self.assertEqual(expected_invoice_title, "Test Invoice 1")

    def test_invoice_total(self):
        invoice= Invoice.objects.get(id=1)
        expected_invoice_total = invoice.get_invoice_total()
        self.assertEqual(expected_invoice_total, 80)

    def test_invoice_str_method(self):
        invoice = Invoice.objects.get(id=1)
        expected_invoice_str = f'{invoice.title} - {invoice.invoice_total}'
        self.assertEqual(expected_invoice_str, "Test Invoice 1 - 80.00")

    def test_invoice_repr_method(self):
        invoice = Invoice.objects.get(id=1)
        expected_invoice_repr = repr(invoice)
        self.assertEqual(expected_invoice_repr,
                         "<Invoice: Test Client - Test Invoice 1>")


class ClientTests(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='testuser',
            email='test@email.com',
            password='secretpassword'
        )

        self.client1 = Client.objects.create(
            first_name="Test", last_name="Client", email="test@example.com",
            company="Xcorp", address1="1234 Paradise Lane",
            address2="Good Street", country="Zimbabwe",
            phone_number="+263772873063",
            created_by=self.user
        )

        self.invoice = Invoice.objects.create(
            title="Test Invoice 1",
            user=self.user,
            client=self.client1,
            create_date=datetime.datetime.now()
        )

        self.invoice_item1 = InvoiceItem.objects.create(
            invoice=self.invoice,
            item="Test Line Item",
            quantity=3,
            rate=20,
            tax=0,
        )

        self.invoice_item2 = InvoiceItem.objects.create(
            invoice=self.invoice,
            item="Test Line Item 2",
            quantity=1,
            rate=20,
            tax=0,
        )

    def test_client_object_content(self):
        client = Client.objects.get(id=1)
        expected_first_name = f'{client.first_name}'
        expected_last_name = f'{client.last_name}'
        expected_created_by_user = f'{client.created_by}'
        invoiced_to_client = client.invoice_set.all()

        self.assertEqual(expected_first_name, "Test")
        self.assertEqual(expected_last_name, "Client")
        self.assertEqual(expected_created_by_user, "testuser")
        self.assertEqual(len(invoiced_to_client), 1)

    def test_client_object_repr(self):
        client1 = Client.objects.get(id=1)
        self.assertEqual(repr(client1), "Client: Test Client")

    def test_client_str(self):
        client1 = Client.objects.get(id=1)
        self.assertEqual(str(client1), "Test Client")


class ViewsLoggedInTests(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='testuser',
            email='test@email.com',
            password='secretpassword'
        )

        self.client1 = Client.objects.create(
            first_name="Test", last_name="Client", email="test@example.com",
            company="Xcorp", address1="1234 Paradise Lane",
            address2="Good Street", country="Zimbabwe",
            phone_number="+263772873063",
            created_by=self.user
        )

        self.invoice = Invoice.objects.create(
            title="Test Invoice 1",
            user=self.user,
            client=self.client1,
            create_date=datetime.datetime.now()
        )

        self.client.login(username='testuser', password='secretpassword')


    def test_invoice_list_view(self):
        response = self.client.get(reverse('invoice-list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Invoicing App")
        self.assertTemplateUsed(response, 'dashboard.html')

    def test_invoice_create_view(self):
        response = self.client.get(reverse('new-invoice'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'new_invoice.html')

    def test_invoice_detail_view(self):
        response = self.client.get(reverse('invoice-detail', args=[1]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'invoice_detail.html')

    def test_invoice_update_view(self):
        response = self.client.get(reverse('invoice-edit', args=[1]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'edit_invoice.html')

    def test_invoice_delete_view(self):
        response = self.client.get(reverse('invoice-delete', args=[1]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'confirm_delete_invoice.html')

    def test_add_client_view(self):
        response = self.client.get(reverse('new-client'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'new_client.html')

    def test_client_list_view(self):
        response = self.client.get(reverse('client-list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'clients.html')

    def test_client_update_view(self):
        response = self.client.get(reverse('client-edit', args=[1]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'edit_client.html')

    def test_client_detail_view(self):
        response = self.client.get(reverse('client-detail', args=[1]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'client_detail.html')


class ViewsLoggedOutTests(TestCase):

    def test_invoice_list_view(self):
        response = self.client.get(reverse('invoice-list'))
        self.assertEqual(response.status_code, 302)

    def test_invoice_create_view(self):
        response = self.client.get(reverse('new-invoice'))
        self.assertEqual(response.status_code, 302)


    def test_invoice_detail_view(self):
        response = self.client.get(reverse('invoice-detail', args=[1]))
        self.assertEqual(response.status_code, 302)


    def test_invoice_update_view(self):
        response = self.client.get(reverse('invoice-edit', args=[1]))
        self.assertEqual(response.status_code, 302)


    def test_invoice_delete_view(self):
        response = self.client.get(reverse('invoice-delete', args=[1]))
        self.assertEqual(response.status_code, 302)


    def test_add_client_view(self):
        response = self.client.get(reverse('new-client'))
        self.assertEqual(response.status_code, 302)

    def test_client_list_view(self):
        response = self.client.get(reverse('client-list'))
        self.assertEqual(response.status_code, 302)

    def test_client_update_view(self):
        response = self.client.get(reverse('client-edit', args=[1]))
        self.assertEqual(response.status_code, 302)

    def test_client_detail_view(self):
        response = self.client.get(reverse('client-detail', args=[1]))
        self.assertEqual(response.status_code, 302)


class ViewsLoggedInNewUserTests(TestCase):
    # These tests test website functionality for a new user who hasn't added
    # data

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='testuser',
            email='test@email.com',
            password='secretpassword'
        )

        # self.client1 = Client.objects.create(
        #     first_name="Test", last_name="Client", email="test@example.com",
        #     company="Xcorp", address1="1234 Paradise Lane",
        #     address2="Good Street", country="Zimbabwe",
        #     phone_number="+263772873063",
        #     created_by=self.user
        # )
        #
        # self.invoice = Invoice.objects.create(
        #     title="Test Invoice 1",
        #     user=self.user,
        #     client=self.client1,
        #     create_date=datetime.datetime.now()
        # )

        self.client.login(username='testuser', password='secretpassword')

    def test_empty_client_list_view(self):
        response = self.client.get(reverse('client-list'))
        self.assertContains(response, "You have not created any clients yet")


