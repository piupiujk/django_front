from django.urls import path
from .views import AsyncProxyView, AsyncTokenObtainPairView, AsyncTokenRefreshView
from django_prometheus.exports import ExportToDjangoView

urlpatterns = [
    path('token/', AsyncTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', AsyncTokenRefreshView.as_view(), name='token_refresh'),
    path('<path:path>', AsyncProxyView.as_view(), name='async_proxy'),
    path('metrics/', ExportToDjangoView.as_view(), name='prometheus_metrics'),
]