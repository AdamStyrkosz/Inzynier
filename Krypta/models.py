import datetime
import os

from django.conf import settings
from django.db import models
# Create your models here.
from django.db.models import CASCADE


def filepath(request, filename):
    old_filename = filename
    timeNow = datetime.datetime.now().strftime("%Y%m%d%H:%M:%S")
    filename = "%s%s" % (timeNow, old_filename)
    return os.path.join("uploads/", filename)


class Wpis(models.Model):
    ARTICLE_TYPES = (
        ('NEWS', 'Aktualności'),
        ('EDUCATION', 'Artukuły edukacyjne')
    )
    id = models.AutoField(primary_key=True)
    type = models.CharField(max_length=16, choices=ARTICLE_TYPES)
    tytul = models.CharField(max_length=50)
    zawartosc = models.TextField(max_length=5000)
    opis = models.TextField(max_length=250)
    obraz = models.ImageField(upload_to=filepath)
    data_utworzenia = models.DateTimeField()

    def __str__(self):
        return str(self.tytul)

    class Meta:
        verbose_name = "Wpis"
        verbose_name_plural = "Wpisy"


class Comment(models.Model):
    news = models.ForeignKey(Wpis, related_name='news', on_delete=CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=CASCADE)
    content = models.TextField(max_length=512)
    publication_date = models.DateTimeField(auto_now=True)


class Cryptocurrency(models.Model):
    id = models.CharField(max_length=10, unique=True, primary_key=True)
    name = models.CharField(max_length=32)
    description = models.TextField(max_length=2000)
    website = models.URLField(null=True)
    whitepaper = models.URLField(null=True)
    connected_news = models.ManyToManyField(Wpis, related_name="wpis", blank=True)

    def __str__(self):
        return self.id

    class Meta:
        verbose_name = "Kryptowaluta"
        verbose_name_plural = "Kryptowaluty"


class CryptocurrencyExchangeModel(models.Model):
    BUY = "BUY"
    SELL = "SELL"
    TRANSACTION_TYPES = (
        (BUY, "Kupno"),
        (SELL, "Sprzedaż")
    )

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    count = models.FloatField()
    cryptocurrency = models.ForeignKey(Cryptocurrency, on_delete=models.CASCADE)
    price = models.FloatField()
    date_of_transaction = models.DateField()
    transaction_type = models.CharField(max_length=32, choices=TRANSACTION_TYPES, default=BUY)

    def __str__(self):
        return f"{self.user} | {self.cryptocurrency.name} | Cena: {self.price} | Typ: {self.transaction_type} | Data: {self.date_of_transaction}"

    class Meta:
        verbose_name = "Kupno i sprzedaż"
        verbose_name_plural = "Kupno i sprzedaż"
