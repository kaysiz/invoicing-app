from django.urls import path
from . import views


urlpatterns = [
    path('', views.InvoiceListView.as_view(), name='home'),
]
