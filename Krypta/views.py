from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView
from django.http import Http404
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import View, UpdateView
from nomics import Nomics
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .forms import ExchangeForm, UserRegistration
from .models import CryptocurrencyExchangeModel, Wpis, Cryptocurrency, Comment
from .serializers import CryptoDetailSerializer, ExchangeSerializer, CommentSerializer

# Create your views here.

nomics = Nomics("7e9fbd09298ee1d741b02b628020b0bb7a6819e8")


# API VIEWS
class CommentAddView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(status=200)


class ExchangeViewSet(LoginRequiredMixin, viewsets.ModelViewSet):
    queryset = CryptocurrencyExchangeModel.objects.all()
    serializer_class = ExchangeSerializer

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)


class CryptocurrencyDetailView(APIView):
    def get(self, request, id):
        queryset = Cryptocurrency.objects.get(id=id)
        serializer = CryptoDetailSerializer(queryset)
        return Response(serializer.data)


class CryptocurrencyIndexAPI(APIView):
    def get(self, request):
        data = nomics.Currencies.get_currencies(
            ids="BTC,ETH,ADA,BNB,XRP,SOL,DOT,LTC", interval="1d,7d"
        )
        if data:
            for i in range(len(data)):
                data[i]["1d"]["price_change_pct"] = str(
                    float(data[i]["1d"]["price_change_pct"]) * 100
                )
                data[i]["7d"]["price_change_pct"] = str(
                    float(data[i]["7d"]["price_change_pct"]) * 100
                )
            return Response(data)
        else:
            return Response("Brak danych na serwerze")


class CryptocurrencyAllAPI(APIView):
    def get(self, request):
        data = nomics.Currencies.get_currencies(
            ids="BTC,ETH,ADA,BNB,XRP,SOL,DOT,DOGE,UNI,AVAX,LUNA,LINK,ALGO,LTC,"
                "BCH,ATOM,MATIC",
            interval="1d,7d",
        )
        if data:
            for i in range(len(data)):
                data[i]["1d"]["price_change_pct"] = str(
                    float(data[i]["1d"]["price_change_pct"]) * 100
                )
                data[i]["7d"]["price_change_pct"] = str(
                    float(data[i]["7d"]["price_change_pct"]) * 100
                )
            return Response(data)
        else:
            return Response("Brak danych na serwerze")


# HTML VIEWS
class Index(View):
    def get(self, request):
        wpisy = Wpis.objects.order_by("-data_utworzenia")[:3]
        context = {
            "wpisy": wpisy,
        }
        return render(request, "Krypta/index.html", context)


class CryptoDetail(View):
    def get(self, request, id):
        crypto = Cryptocurrency.objects.filter(id=id)
        if crypto:
            crypto = Cryptocurrency.objects.get(id=id)
            wpisy = crypto.connected_news.all()
            datafromapi = nomics.Currencies.get_currencies(ids=id, interval="1d")
            apidata = {
                "price": datafromapi[0]["price"],
                "high": datafromapi[0]["high"],
                "delta": str(
                    float(datafromapi[0]["high"]) - float(datafromapi[0]["price"])
                ),
                "image": datafromapi[0]["logo_url"],
            }
            context = {"cryptocurrency": crypto, "wpisy": wpisy, "apidata": apidata}
            return render(request, "Krypta/crypto_detail.html", context)
        return render(request, "Krypta/brak_danych.html")


class Dashboard(LoginRequiredMixin, View):
    def get(self, request):
        balance = 0
        value_diff = 0
        symbols = ""

        form = ExchangeForm()
        cryptocurencies = CryptocurrencyExchangeModel.objects.filter(user=request.user).order_by(
            '-date_of_transaction').values()

        for item in cryptocurencies:
            if str(item['cryptocurrency_id']) not in symbols:
                symbols += f"{str(item['cryptocurrency_id'])},"

        datafromapi = nomics.Currencies.get_currencies(ids=symbols, interval="1d")
        crypto_to_price_mapping = {}
        for crypto in datafromapi:
            crypto_to_price_mapping[crypto['currency']] = crypto['price']

        for crypto in cryptocurencies:
            crypto['actual_price'] = float(crypto_to_price_mapping[crypto['cryptocurrency_id']])
            crypto['price_diff'] = (float(crypto['actual_price'])) * float(crypto['count']) - (
                    float(crypto['price']) * float(crypto['count']))
            value_diff += crypto['price_diff']
            if crypto['transaction_type'] == CryptocurrencyExchangeModel.BUY:
                balance += crypto['actual_price'] * crypto['count']

        context = {
            "user": request.user,
            "cryptocurrencies": cryptocurencies,
            "balance": balance,
            "value_diff": value_diff,
            "form": form
        }
        return render(request, "Krypta/dashboard.html", context)

    def post(self, request):
        form = ExchangeForm(request.POST)
        if form.is_valid():
            new_user = form.save(commit=False)
            new_user.user = request.user
            new_user.save()
            return redirect("dashboard")
        return render(request, "Krypta/dashboard.html", {"form": form})


class CryptocurrencyList(View):
    def get(self, request):
        return render(request, "Krypta/kursy.html")


class NewsArticleView(View):
    def get(self, request):
        queryset = Wpis.objects.filter(type='NEWS').order_by("-data_utworzenia")
        content = {
            'news': queryset
        }
        return render(request, 'Krypta/wpis_list.html', content)


class EducationArticaleView(View):
    def get(self, request):
        queryset = Wpis.objects.filter(type='EDUCATION').order_by("-data_utworzenia")
        content = {
            'news': queryset
        }
        return render(request, 'Krypta/wpis_list.html', content)


class WpisDetail(View):
    def get(self, request, pk, *args, **kwargs):
        content = {
            'wpis': Wpis.objects.get(id=pk),
            'comments': Comment.objects.filter(news=pk).order_by('-publication_date')
        }
        return render(request, 'Krypta/wpis_detail.html', content)


class UserDetail(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, "Krypta/user_detail.html")


class CustomLogin(LoginView):
    template_name = "Krypta/login.html"
    fields = "__all__"
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy("index")


class RegisterPage(View):
    def get(self, request):
        form = UserRegistration()
        context = {"form": form}
        return render(request, "Krypta/register.html", context)

    def post(self, request):
        form = UserRegistration(request.POST)
        if form.is_valid():
            user = form.save(commit=True)
            login(request, user)
            return redirect("profil")
        return render(request, "Krypta/register.html", {"form": form})


class EdycjaWpisu(UpdateView):
    template_name = "Krypta/edycja_wpisu.html"
    model = Wpis
    fields = (
        'tytul',
        'zawartosc',
        'opis'
    )
    success_url = reverse_lazy("aktualnosci")

    def get(self, request, pk):
        if request.user.is_superuser:
            return super(EdycjaWpisu, self).get(self, request, pk)
        else:
            return redirect("index")


class EdycjaProfilu(UpdateView):
    template_name = "Krypta/edycja_uzytkownika.html"
    model = User
    fields = ("username", "first_name", "last_name")
    success_url = reverse_lazy("profil")

    def get(self, request, pk):
        if request.user.id == pk:
            return super(EdycjaProfilu, self).get(self, request, pk)
        return redirect("index")


class CryptocurrencyExchangeUpdateView(UpdateView):
    template_name = "Krypta/edycja_wpisu.html"
    model = CryptocurrencyExchangeModel
    fields = [
        "cryptocurrency",
        "count",
        "price",
        "date_of_transaction",
    ]
    labels = {
        "cryptocurrency": "Kryptowaluta",
        "count": "Ilo????",
        "price": "Cena",
        "date_of_transaction": "Data transakcji"
    }
    success_url = reverse_lazy("dashboard")

    def get(self, request, pk):
        try:
            obj = CryptocurrencyExchangeModel.objects.get(user=request.user, id=pk)
        except CryptocurrencyExchangeModel.DoesNotExist:
            raise Http404("No exchange matches the given query.")
        if obj:
            return super(CryptocurrencyExchangeUpdateView, self).get(self, request, pk)
        else:
            return redirect("index")
