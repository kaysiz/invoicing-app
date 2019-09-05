from django.urls import path
from . import views


urlpatterns = [
    path('', views.InvoiceListView.as_view(), name='home'),
    path('dashboard/', views.DashboardView.as_view(), name='dashboard'),
    path('invoices/new/', views.InvoiceCreateView.as_view(), name="new-invoice"),
]
