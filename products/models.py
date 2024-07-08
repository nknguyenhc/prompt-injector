from django.db import models

class Pet(models.Model):
    name = models.CharField(max_length=100)
    price = models.FloatField()
    popularity = models.CharField(max_length=20)
    stock_status = models.CharField(max_length=20)

class Book(models.Model):
    name = models.CharField(max_length=100)
    price = models.FloatField()
    popularity = models.CharField(max_length=20)
    stock_status = models.CharField(max_length=20)

class Movie(models.Model):
    name = models.CharField(max_length=100)
    price = models.FloatField()
    popularity = models.CharField(max_length=20)
    stock_status = models.CharField(max_length=20)

class Flag(models.Model):
    value = models.CharField(max_length=100)
