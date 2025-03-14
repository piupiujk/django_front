from django.db import models
from django.contrib.auth.models import User

class Docs(models.Model):
    file_path = models.CharField(max_length=200)
    size = models.IntegerField()

class UsersToDocs(models.Model):
    username = models.CharField(max_length=100)
    docs_id = models.ForeignKey(Docs, on_delete=models.CASCADE, related_name='docs_id')

class Price(models.Model):
    file_type = models.CharField(max_length=100)
    price = models.FloatField()

class Cart(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    docs_id = models.ForeignKey(Docs, on_delete=models.CASCADE)
    order_price = models.FloatField()
    payment = models.BooleanField(default=False)