import os
from django.shortcuts import render, get_object_or_404, redirect, HttpResponse
from .models import Consignment, Carpass, Contact, Document
from .forms import ConsignmentForm, CarpassForm, DocumentForm
from django.views.decorators.http import require_POST
from datetime import datetime
from django.conf import settings
from django.http import HttpResponse, Http404
from urllib.parse import quote


contact_test_id = 20263  # для тестовой версии, пока не добавлена страница аутентификации

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

    return render(request,
                  'client_service/consignment/list.html',
                  {'consignments': consignments,
                   'documents': documents})


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

    return render(request,
                  'client_service/carpass/list.html',
                  {'carpasses': carpasses,
                   'documents': documents})


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
