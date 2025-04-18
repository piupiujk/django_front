from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class ProxyLog(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    ip_address = models.GenericIPAddressField()
    method = models.CharField(max_length=10)
    path = models.TextField()
    status_code = models.IntegerField()
    request_headers = models.JSONField()
    request_body = models.TextField(null=True, blank=True)
    response_headers = models.JSONField()
    response_body = models.TextField(null=True, blank=True)
    response_time = models.FloatField()
    target_url = models.TextField()
    from_cache = models.BooleanField(default=False)

    class Meta:
        indexes = [
            models.Index(fields=['-timestamp']),
            models.Index(fields=['user']),
            models.Index(fields=['method']),
        ]