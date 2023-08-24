import os
from django.shortcuts import render, get_object_or_404, redirect, HttpResponse
from .models import Consignment, Carpass, Contact, Document
from .forms import ConsignmentForm, CarpassForm, DocumentForm
from .forms import ConsignmentFiltersForm, CarpassFiltersForm
from django.views.decorators.http import require_POST
from datetime import datetime
from django.conf import settings
from django.http import HttpResponse, Http404
from urllib.parse import quote


contact_test_id = 25201  # для тестовой версии, пока не добавлена страница аутентификации

#  CONSIGNMENT ******************************************
def consignment_list(request):
    try:
        consignments = Consignment.objects.filter(posted=True).filter(contact=contact_test_id)
    except:
        consignments = ''

    try:
        key_id_list = consignments.values_list("key_id", flat=True)
        documents = Document.objects.filter(guid_partia__in=key_id_list)
    except:
        documents = ''

    # фильтрация данных
    form_filters = ConsignmentFiltersForm()
    if request.method == 'POST':
        form_filters = ConsignmentFiltersForm(data=request.POST)
        if form_filters.is_valid():
            cd = form_filters.cleaned_data
            if cd['key_id']:
                consignments = consignments.filter(key_id=cd['key_id'])
            if cd['contact_name']:
                consignments = consignments.filter(contact_name=cd['contact_name'])
            if cd['broker_name']:
                consignments = consignments.filter(broker_name=cd['broker_name'])
            if cd['nttn']:
                consignments = consignments.filter(nttn=cd['nttn'])
            if cd['dkd']:
                consignments = consignments.filter(dkd=cd['dkd'])
            if cd['dater_from']:
                consignments = consignments.filter(dater__gte=cd['dater_from'])
            if cd['dater_to']:
                consignments = consignments.filter(dater__lte=cd['dater_to'])
            if cd['dateo_from']:
                consignments = consignments.filter(dateo__gte=cd['dateo_from'])
            if cd['dateo_to']:
                consignments = consignments.filter(dateo__lte=cd['dateo_to'])
            if cd['car']:
                consignments = consignments.filter(car=cd['car'])
            if cd['on_terminal']:
                consignments = consignments.filter(dateo__isnull=True)
            else:
                consignments = consignments.filter(dateo__isnull=False)

    return render(request,
                  'client_service/consignment/list.html',
                  {'consignments': consignments,
                   'documents': documents,
                   'form_filters': form_filters, })


def consignment_update(request, id):
    consignment = get_object_or_404(Consignment, id=id)
 
    try:
        documents = Document.objects.filter(guid_partia=consignment.key_id)
    except:
        documents = ''
    
    data = {}
    data['block_name'] = 'Партия товаров'  # 'ПАРТИЯ ТОВАРОВ'
    data['entity'] = 'consignment'
    data['id'] = consignment.key_id

    form = ConsignmentForm(instance=consignment)

    return render(request,
                  'client_service/update_universal.html',
                  {'form': form,
                   'data': data, 
                   'entity': consignment,
                   'documents': documents, })


def consignment_close(request, id):
    consignment = get_object_or_404(Consignment, id=id)

    if request.method == 'POST':
        return redirect('/client_service/consignments')
    
    return render(request,
                  'client_service/consignment/close.html',
                  {'consignment': consignment})


#  CARPASS ******************************************
def carpass_list(request):
    try:
        carpasses = Carpass.objects.filter(posted=True).filter(contact=contact_test_id)
    except:
        carpasses = ''

    try:
        id_enter_list = carpasses.values_list("id_enter", flat=True)
        documents = Document.objects.filter(id_enter__in=id_enter_list)
    except:
        documents = ''

    # фильтрация данных
    form_filters = CarpassFiltersForm()
    if request.method == 'POST':
        form_filters = CarpassFiltersForm(data=request.POST)
        if form_filters.is_valid():
            cd = form_filters.cleaned_data
            if cd['id_enter']:
                carpasses = carpasses.filter(id_enter=cd['id_enter'])
            if cd['ncar']:
                carpasses = carpasses.filter(ncar=cd['ncar'])
            if cd['ntir']:
                carpasses = carpasses.filter(ntir=cd['ntir'])
            if cd['nkont']:
                carpasses = carpasses.filter(nkont=cd['nkont'])
            if cd['dateen_from']:
                carpasses = carpasses.filter(dateen__gte=cd['dateen_from'])
            if cd['dateen_to']:
                carpasses = carpasses.filter(dateen__lte=cd['dateen_to'])

    return render(request,
                  'client_service/carpass/list.html',
                  {'carpasses': carpasses,
                   'documents': documents,
                   'form_filters': form_filters, })


def carpass_update(request, id):
    carpass = get_object_or_404(Carpass, id=id)
 
    try:
        documents = Document.objects.filter(id_enter=carpass.id_enter)
    except:
        documents = ''

    data = {}
    data['block_name'] = 'Пропуск'  # 'ПРОПУСК' #
    data['entity'] = 'carpass'
    data['id'] = carpass.id_enter
    

    form = CarpassForm(instance=carpass)

    return render(request,
                  'client_service/update_universal.html',
                  {'form': form,
                   'data': data, 
                   'entity': carpass,
                   'documents': documents, })


def carpass_close(request, id):
    carpass = get_object_or_404(Carpass, id=id)

    if request.method == 'POST':
        return redirect('/client_service/carpass')
    
    return render(request,
                  'client_service/carpass/close.html',
                  {'carpass': carpass})


#  DOCUMENT ******************************************
def document_update(request, id):
    document = get_object_or_404(Document, id=id)
    if document.guid_partia:
        entity = get_object_or_404(Consignment, key_id=document.guid_partia)
    elif document.id_enter:
        entity = get_object_or_404(Carpass, id_enter=document.id_enter)

    form = DocumentForm(instance=document)

    return render(request,
                  'client_service/document/update.html',
                  {'form': form,
                   'document': document,
                   'entity': entity, })


def document_close(request, id):
    document = get_object_or_404(Document, id=id)
    if document.guid_partia:
        entity = get_object_or_404(Consignment, key_id=document.guid_partia)
        entity_title = 'consignments'
    elif document.id_enter:
        entity = get_object_or_404(Carpass, id_enter=document.id_enter)
        entity_title = 'carpass'
    # consignment = get_object_or_404(Consignment, key_id=document.guid_partia)

    
    if request.method == 'POST':
        return redirect(f'/client_service/{entity_title}/{entity.id}/update')
    
    return render(request,
                  'client_service/document/close.html',
                  {'document': document})


def document_download(request, id):
    """
    Скачивает документ
    """
    document = get_object_or_404(Document, id=id)
    path = str(document.file)
    file_path = os.path.join(settings.MEDIA_ROOT, path)
    print(file_path)
    if os.path.exists(file_path):
        with open(file_path, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type="text/plain")
            # response['Content-Disposition'] = 'attachment; filename=' + os.path.basename(file_path)
            response['Content-Disposition'] = "attachment; filename*=utf-8''{}".format(quote(os.path.basename(file_path)))
            return response
    return Http404
