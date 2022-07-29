from django.db import models
from django.contrib.auth.models import User


class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=200, null=True)
    email = models.CharField(max_length=200, null=True)

    def __str__(self):
        return self.name


class mediaContent(models.Model):
    title = models.CharField(max_length=250, null=True)
    category = models.CharField(max_length=30, null=True)
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, blank=True, null=True)


class userData(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, blank=True, null=True)
    title = models.CharField(max_length=250, null=True)
    uploadedFile = models.FileField(upload_to="Uploaded User Files/")


class token(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, blank=True, null=True)
    generated_token = models.CharField(max_length=250, null=True)
