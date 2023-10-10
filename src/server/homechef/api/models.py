from django.db import models


# Create your models here.

class Uchenik(models.Model):
    uspeh = models.CharField(max_length=100)
    creativnost = models.CharField(max_length=100)
    potencial = models.CharField(max_length=100)
