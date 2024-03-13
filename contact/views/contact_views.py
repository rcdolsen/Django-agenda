# from django.http import Http404
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render

from contact.models import Contact


def index(request):
    contacts = Contact.objects \
        .filter(show=True) \
        .order_by("-id")  # [0:10]

    paginator = Paginator(contacts, 25)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    # print(contacts.query)

    context = {
        'page_obj': page_obj,
        'site_title': 'Contacts - '
    }

    return render(
        request,
        'contact/index.html',
        context
    )


def contact(request, contact_id):
    # single_contact = Contact.objects.filter(pk=contact_id).first()

    # if single_contact is None:
    #     raise Http404()

    # atalho do django
    single_contact = get_object_or_404(
        # Contact.objects.filter(pk=contact_id)
        Contact, pk=contact_id, show=True
    )

    contact_name = f'{single_contact.first_name} {single_contact.last_name} - '

    context = {
        'contact': single_contact,
        'site_title': contact_name
    }
    return render(
        request,
        'contact/contact.html',
        context
    )


def search(request):
    search_value = request.GET.get('q', '').strip()

    if search_value == '':
        return redirect('contact:index')

    contacts = Contact.objects \
        .filter(show=True) \
        .filter(
            Q(first_name__icontains=search_value) |
            Q(last_name__icontains=search_value) |
            Q(phone__icontains=search_value) |
            Q(email__icontains=search_value)
        ) \
        .order_by("-id")  # [0:10]

    paginator = Paginator(contacts, 25)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    # print(contacts.query)

    context = {
        'page_obj': page_obj,
        'site_title': 'search - ',
        'search_value': search_value,
    }

    return render(
        request,
        'contact/index.html',
        context
    )
