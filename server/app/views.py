from django.shortcuts import render
from django.core.files.storage import FileSystemStorage

# Create your views here.
from django.http import HttpResponse


def index(request):
    return render(request, 'index.html')


def upload(request):
    if request.method == 'POST':
        uploaded_files = request.FILES['document']
        fs = FileSystemStorage()
        fs.save(uploaded_files.name, uploaded_files)
    return render(request, 'upload.html')
