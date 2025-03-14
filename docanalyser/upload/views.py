from django.shortcuts import render
from django.http import HttpResponse


from django.shortcuts import render, redirect
from .models import Docs
from .forms import DocumentForm

def home(request):
    documents = Docs.objects.all()  # Получаем все загруженные картинки
    return render(request, 'upload/home.html', {'documents': documents})

def upload_document(request):
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = DocumentForm()
    return render(request, 'upload/upload.html', {'form': form})
