from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator
from django.db.models import Q, Value
from django.db.models.functions import Concat
from django.contrib import messages
from .models import Contact


def index(request):
    contacts = Contact.objects.order_by('name')
    paginator = Paginator(contacts, 5)

    page_number = request.GET.get('page')
    contacts = paginator.get_page(page_number)
    
    return render(request, 'contacts/index.html', {
        'contacts': contacts
    })


def view_contact(request, contact_id):
    contact = get_object_or_404(Contact, id=contact_id)

    return render(request, 'contacts/view_contact.html', {
        'contact': contact
    })


def search(request):
    parameter = request.GET.get('parameter')

    if parameter is None or not parameter:
        messages.add_message(request, messages.ERROR, 'Search field cannot be empty.')
        return redirect('index')

    fields = Concat('name', Value(' '), 'lastname')

    contacts = Contact.objects.annotate(
        fullname = fields,
    ).filter(
        Q(fullname__icontains = parameter) |
        Q(phone_number__icontains = parameter)
    )

    paginator = Paginator(contacts, 5)

    page_number = request.GET.get('page')
    contacts = paginator.get_page(page_number)
    
    return render(request, 'contacts/index.html', {
        'contacts': contacts
    })
