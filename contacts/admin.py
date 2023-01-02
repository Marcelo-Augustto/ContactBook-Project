from django.contrib import admin
from .models import Category, Contact


class ContactAdmin(admin.ModelAdmin):
    search_fields = ('id', 'name', 'lastname', 'phone_number', 'email', 'creation_date')
    list_display = ('id', 'name', 'lastname', 'phone_number', 'email', 'creation_date', 'category')
    list_display_links = ('id', 'name', 'lastname', 'email')
    list_filter = ('category',)
    list_per_page: 15


admin.site.register(Category)
admin.site.register(Contact, ContactAdmin)
