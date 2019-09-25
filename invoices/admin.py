from django.contrib import admin
from .models import Invoice, Client


admin.site.register(Invoice)
admin.site.register(Client)
