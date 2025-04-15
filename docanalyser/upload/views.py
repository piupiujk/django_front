import base64
import json

import requests
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render
from django.http import HttpResponse, Http404
from django.core.files.storage import default_storage

from django.shortcuts import render, redirect

from .api_client import call_fastapi
from .models import Docs, UsersToDocs
from .forms import UploadFileForm, DeleteDocumentForm


def home(request):
    documents = Docs.objects.all()  # Получаем все загруженные картинки
    return render(request, 'upload/home.html', {'documents': documents, 'request': request})


@login_required
def upload_document(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_file = request.FILES['file']

            file_name = default_storage.save(uploaded_file.name, uploaded_file)
            file_path = uploaded_file.name
            file_size = uploaded_file.size

            uploaded_file.seek(0)
            with open(f'media/{file_path}', "rb") as image_file:
                image_base64 = base64.b64encode(image_file.read()).decode('utf-8')


            # Сохраняем информацию в базу данных
            doc = Docs.objects.create(
                file_path=file_path,
                size=file_size
            )

            UsersToDocs.objects.create(
                user=request.user,
                document=doc
            )

            api_response = call_fastapi(
                'documents/upload_doc',
                method='post',
                data={
                    "id": doc.pk,
                    "image_base64": image_base64
                },
            )

            if not api_response:
                messages.error(request, 'Ошибка обработки документа')
                print('ERROR')
                return redirect('home')

            print("API Response:", api_response)

            return redirect('home')
    else:
        form = UploadFileForm()
    return render(request, 'upload/upload.html', {'form': form})


def is_moderator(user):
    return user.groups.filter(name='Moderators').exists() or user.is_superuser


@user_passes_test(is_moderator)
def delete_document_view(request):
    if request.method == 'POST':
        form = DeleteDocumentForm(request.POST)
        if form.is_valid():
            doc_id = form.cleaned_data['document_id']
            try:
                doc = Docs.objects.get(id=doc_id)
                doc.delete()
                messages.success(request, f'Документ {doc_id} успешно удален')

                api_response = call_fastapi(
                    f'documents/doc_delete/{doc_id}',
                    method='delete',
                )

                if not api_response:
                    messages.error(request, 'Ошибка обработки документа')
                    print('ERROR')
                    return redirect('home')

                print("API Response:", api_response)

                return redirect('delete_document')
            except Docs.DoesNotExist:
                messages.error(request, f'Документ с ID {doc_id} не найден')
    else:
        form = DeleteDocumentForm()

    return render(request, 'upload/delete_document.html', {'form': form})


@login_required
def document_detail(request, doc_id):
    try:
        user_doc = UsersToDocs.objects.get(user=request.user, doc_id=doc_id)
        doc = user_doc.doc
        return render(request, 'upload/document.html', {'doc': doc})
    except UsersToDocs.DoesNotExist:
        raise Http404("Документ не найден или у вас нет доступа")


@login_required
def document_analyse(request, doc_id):
    if request.method == 'GET':
        api_response = call_fastapi(
            f'documents_text/doc_analyse/{doc_id}',
            method='get',
            data={
                "id": doc_id
            },
        )

        if not api_response:
            messages.error(request, 'Ошибка обработки документа')
            print('ERROR')
            return redirect('home')

        print("API Response:", api_response)

    return render(request, 'upload/document_analyse.html')


@login_required
def get_text(request, doc_id):
    if request.method == 'GET':
        api_response = call_fastapi(
            f'documents_text/get_text/{doc_id}',
            method='get',
            data={
                "id": doc_id
            },
        )

        context = {
            'doc_id': doc_id,
            'api_response': api_response
        }

        if not api_response:
            print('ERROR')
            messages.error(request, f"Ошибка при получении текста")
            return render(request, 'upload/get_text.html')

        print("API Response:", api_response)

        # Если статус 202 - успешно
        messages.success(request, f'Текст документа: {api_response["message"]}')
        return render(request, 'upload/get_text.html', context)
    return render(request, 'upload/get_text.html')
