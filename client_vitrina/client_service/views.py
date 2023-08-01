from django.shortcuts import render, get_object_or_404, redirect, HttpResponse
from .models import Consignment, Contact, Document
from .forms import ConsignmentForm, DocumentForm
from django.views.decorators.http import require_POST
from datetime import datetime


#  CONSIGNMENT ******************************************
def consignment_list(request):
    try:
        consignments = Consignment.objects.filter(posted=True).filter(contact=6)
    except:
        consignments = ''

    return render(request,
                  'client_service/consignment/list.html',
                  {'consignments': consignments})


def consignment_update(request, id):
    consignment = get_object_or_404(Consignment, id=id)
 
    try:
        documents = Document.objects.filter(guid_partia=consignment.key_id)
    except:
        documents = ''

    # if request.method == 'POST':
    #     form = ConsignmentForm(request.POST, instance=consignment)
    #     if form.is_valid():
    #         form.save()
    #         return render(request,
    #                     'shv_service/consignment/update.html',
    #                     {'form': form,
    #                      'consignment': consignment,
    #                      'documents': documents})
    # else:
    #     form = ConsignmentForm(instance=consignment)

    form = ConsignmentForm(instance=consignment)

    return render(request,
                  'client_service/consignment/update.html',
                  {
                   'form': form,
                   'consignment': consignment,
                   'documents': documents
                   }
                   )


def consignment_close(request, id):
    consignment = get_object_or_404(Consignment, id=id)

    if request.method == 'POST':
        return redirect('/client_service/consignments')
    
    return render(request,
                  'client_service/consignment/close.html',
                  {'consignment': consignment})


def document_update(request, id):
    document = get_object_or_404(Document, id=id)
    consignment = get_object_or_404(Consignment, key_id=document.guid_partia)

    # if request.method == 'POST':
    #     form = DocumentForm(data=request.POST, files=request.FILES, instance=document)
    #     if form.is_valid():
    #         form.save()
    #         document = get_object_or_404(Document, id=id)
    #         form = DocumentForm(instance=document)

    # else:
    #     form = DocumentForm(instance=document)

    form = DocumentForm(instance=document)

    return render(request,
                  'client_service/document/update.html',
                  {
                   'form': form,
                   'document_id': document.id,
                   'consignment': consignment,
                   })


def document_close(request, id):
    document = get_object_or_404(Document, id=id)
    consignment = get_object_or_404(Consignment, key_id=document.guid_partia)

    
    if request.method == 'POST':
        return redirect(f'/client_service/consignments/{consignment.id}')
    
    return render(request,
                  'client_service/document/close.html',
                  {'document': document})

