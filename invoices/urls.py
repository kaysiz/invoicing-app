from django.urls import path, include
from django.views.generic.base import TemplateView
from .import views


urlpatterns = [
    path('', views.HomePage.as_view(), name='home'),
    # Invoices
    path('invoices/', views.InvoiceListView.as_view(), name='invoice-list'),
    path('invoices/new/', views.InvoiceCreateView.as_view(), name='new-invoice'),
    path('invoices/<int:pk>/', views.InvoiceDetailView.as_view(), name='invoice-detail'),
    path('invoices/edit/<int:pk>/', views.InvoiceUpdateView.as_view(), name='invoice-edit'),
    path('invoices/delete/<int:pk>/', views.InvoiceDeleteView.as_view(), name='invoice-delete'),
    # Clients
    path('clients/', views.ClientListView.as_view(), name='client-list'),
    path('clients/new/', views.ClientCreateView.as_view(), name='new-client'),
    path('clients/<int:pk>/', views.ClientDetailView.as_view(), name='client-detail'),
    path('clients/edit/<int:pk>/', views.ClientUpdateView.as_view(), name='client-edit'),


    # path('logout', )
    # path('create/', views.invoice_create_view),
    # path('new_invoice/<int:invoice_id>/', views.edit_invoice),
]
