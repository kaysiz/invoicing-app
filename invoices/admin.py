from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

from users.forms import CustomUserCreationForm, CustomUserChangeForm
from users.models import CustomUser
from .models import Invoice, Client, InvoiceItem

class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ['email', 'username']


class InvoiceItemsInline(admin.TabularInline):
    model = InvoiceItem


class InvoiceAdmin(admin.ModelAdmin):
    inlines = [
        InvoiceItemsInline,
    ]
    readonly_fields = ('invoice_total',)
    # TODO: Add a custom save method to save invoice totals
    # def save_model(self, request, obj, form, change):
    #     obj.invoice_total = obj.get_invoice_total()
    #     super().save_model(request, obj, form, change)

    # def save_formset(self, request, form, formset, change):
    #     instances = formset.save(commit=False)
    #     for obj in formset.deleted_objects:
    #         obj.delete()
    #     for instance in instances:
    #         instance.invoice.get_invoice_total()
    #         instance.save()
    #     formset.save_m2m()


admin.site.register(Invoice, InvoiceAdmin)
admin.site.register(Client)
admin.site.register(InvoiceItem)
