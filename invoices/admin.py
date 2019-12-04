from django.contrib import admin
from .models import Invoice, Client, InvoiceItems




class InvoiceItemsInline(admin.TabularInline):
    model = InvoiceItems


class InvoiceAdmin(admin.ModelAdmin):
    inlines = [
        InvoiceItemsInline,
    ]
    readonly_fields = ('invoice_total',)


admin.site.register(Invoice, InvoiceAdmin)
admin.site.register(Client)
# admin.site.register(InvoiceItems)
