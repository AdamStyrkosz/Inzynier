from nomics import Nomics
from rest_framework import serializers

from .models import CryptocurrencyExchangeModel, Cryptocurrency

nomics = Nomics("7e9fbd09298ee1d741b02b628020b0bb7a6819e8")


class CryptoDetailSerializer(serializers.ModelSerializer):
    stock_data = serializers.SerializerMethodField()

    class Meta:
        model = Cryptocurrency
        fields = [
            "id",
            "description",
            "website",
            "whitepaper",
            "stock_data",
        ]

    def get_stock_data(self, obj):
        return nomics.Currencies.get_currencies(ids=obj.id)


class ExchangeSerializer(serializers.ModelSerializer):
    class Meta:
        model = CryptocurrencyExchangeModel
        fields = "__all__"
