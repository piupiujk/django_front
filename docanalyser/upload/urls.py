from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('upload/', views.upload_document, name='upload'),
    path('document/<int:doc_id>/', views.document_detail, name='document_detail'),
    path('document/analyse/<int:doc_id>/', views.document_analyse, name='document_analyse'),
    path('delete_document/', views.delete_document_view, name='delete_document'),
    path('get_text/<int:doc_id>/', views.get_text, name='get_text'),
]
