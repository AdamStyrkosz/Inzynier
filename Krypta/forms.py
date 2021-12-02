from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from Krypta.models import CryptocurrencyExchangeModel


class UserRegistration(UserCreationForm):
    class Meta:
        model = User
        fields = (
            "username",
            "first_name",
            "last_name",
            "email",
            "password1",
            "password2",
        )

class ExchangeForm(forms.ModelForm):

    class Meta:
        model = CryptocurrencyExchangeModel
        fields = ("cryptocurrency","count","price","date_of_transaction")
        labels = {
            "cryptocurrency" : "Kryptowaluta",
            "count" : "Ilość",
            "price": "Cena",
            "date_of_transaction": "Data transakcji"
        }
