from django.contrib import admin

from Krypta.models import CryptocurrencyExchangeModel, Wpis, Cryptocurrency, Comment

# Register your models here.
admin.site.register(Wpis)
admin.site.register(Cryptocurrency)
admin.site.register(CryptocurrencyExchangeModel)
admin.site.register(Comment)
