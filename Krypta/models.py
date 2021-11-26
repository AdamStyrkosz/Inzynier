import datetime
import os

from django.db import models


# Create your models here.


def filepath(request, filename):
    old_filename = filename
    timeNow = datetime.datetime.now().strftime("%Y%m%d%H:%M:%S")
    filename = "%s%s" % (timeNow, old_filename)
    return os.path.join("uploads/", filename)


class Wpis(models.Model):
    id = models.AutoField(primary_key=True)
    tytul = models.CharField(max_length=50)
    zawartosc = models.TextField(max_length=5000)
    opis = models.TextField(max_length=250)
    obraz = models.ImageField(upload_to=filepath)
    data_utworzenia = models.DateTimeField()

    def __str__(self):
        return str(self.tytul)


class Cryptocurrency(models.Model):
    id = models.CharField(max_length=10, unique=True, primary_key=True)
    description = models.TextField(max_length=2000)
    website = models.URLField(null=True)
    whitepaper = models.URLField(null=True)
    connected_news = models.ManyToManyField(Wpis, related_name="wpis")

    def __str__(self):
        return self.id
