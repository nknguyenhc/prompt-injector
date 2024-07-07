from django.db import models

class Pet(models.Model):
    name = models.CharField(max_length=100)
    price = models.FloatField()

class Book(models.Model):
    name = models.CharField(max_length=100)
    price = models.FloatField()

class Movie(models.Model):
    name = models.CharField(max_length=100)
    price = models.FloatField()

class Flag(models.Model):
    value = models.CharField(max_length=100)
