from django.db import models
from django.contrib.auth.models import User

class Docs(models.Model):
    file_path = models.CharField(max_length=200)
    size = models.IntegerField()

class UsersToDocs(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_docs')
    document = models.ForeignKey(Docs, on_delete=models.CASCADE, related_name='doc_users')

    class Meta:
        unique_together = ('user', 'document')

class Price(models.Model):
    file_type = models.CharField(max_length=100)
    price = models.FloatField()

class Cart(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    docs_id = models.ForeignKey(Docs, on_delete=models.CASCADE)
    order_price = models.FloatField()
    payment = models.BooleanField(default=False)