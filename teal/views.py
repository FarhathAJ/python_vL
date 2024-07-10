from django.shortcuts import render
from . import importdata
from . import teal_vl_graph_integrate
from django.core.files.storage import FileSystemStorage
import json
import os
from django.conf import settings
from django.http import HttpResponseRedirect



def container_view(request):
    importdata.import_data()
    global remaining
    global nos
    global no_of_pallets

    if request.method == 'POST':
        options = json.loads(request.POST.get('options', '[]'))
        uploaded_file = request.FILES.get('file', None)
        save_path = os.path.join(settings.MEDIA_ROOT)

        fs = FileSystemStorage(location=save_path)
        if not fs.exists(uploaded_file.name):
            fs.save(uploaded_file.name, uploaded_file)
        remaining,nos,no_of_pallets=teal_vl_graph_integrate.input_data(uploaded_file, options)
        return HttpResponseRedirect("/pdfview/")
    context={
        'no_of_pallets':globals().get('no_of_pallets',0)
    }
    return render(request, 'index.html',context)


def pdf_view(request):
    context={
        'remaining':globals().get('remaining',None),
        'nos':globals().get('nos',None)
    }
    return render(request,'pdfview.html',context)
