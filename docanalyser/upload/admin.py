from django.contrib import admin
from .models import Docs, UsersToDocs, Price

@admin.register(Docs)
class DocsAdmin(admin.ModelAdmin):
    list_display = ('file_path', 'size')
    search_fields = ('file_path',)

@admin.register(UsersToDocs)
class UserToDocsAdmin(admin.ModelAdmin):
    list_display = ('user', 'document')
    list_filter = ('user',)