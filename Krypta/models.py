import datetime
import os

from django.db import models


# Create your models here.

def filepath(request, filename):
    old_filename = filename
    timeNow = datetime.datetime.now().strftime('%Y%m%d%H:%M:%S')
    filename = "%s%s" % (timeNow, old_filename)
    return os.path.join('uploads/', filename)

class Wpis(models.Model):
    id = models.AutoField(primary_key = True)
    tytul = models.CharField(max_length=50)
    zawartosc = models.TextField(max_length=5000)
    obraz = models.ImageField(upload_to=filepath)
    data_utworzenia = models.DateTimeField()

    def __str__(self):
        return str(self.tytul)

class Cryptocurrency(models.Model):
    id = models.AutoField(primary_key = True)
    name = models.CharField(max_length=20)
    short_name = models.CharField(max_length=5)

    def __str__(self):
        return self.name

class CryptoHistorical(models.Model):
    id = models.AutoField(primary_key = True)
    cryptocurrency = models.ForeignKey(Cryptocurrency,on_delete=models.CASCADE)
    price = models.DecimalField(decimal_places=2, max_digits=20)
    datetime = models.DateTimeField()

    def __str__(self):
        return str(self.datetime)