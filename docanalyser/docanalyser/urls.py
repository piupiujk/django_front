from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.contrib.auth import views as auth_views
from django.conf.urls.static import static

urlpatterns = ([
    path('', include('upload.urls')),
    path('admin/', admin.site.urls),
    path('auth/', include(('accounts.urls', 'accounts'), namespace='accounts'))
])

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
