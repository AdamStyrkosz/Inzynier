from django.contrib.auth import login
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import View, FormView, UpdateView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from nomics import Nomics
from rest_framework import permissions
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import Wpis
from .forms import UserRegistration

# Create your views here.

nomics = Nomics('7e9fbd09298ee1d741b02b628020b0bb7a6819e8')


# API VIEWS
class CryptocurrencyIndexAPI(APIView):

    def get(self, request):
        data = nomics.Currencies.get_currencies(ids="BTC,ETH,ADA,BNB,XRP,SOL,DOT,LTC", interval="1d,7d")
        if data:
            for i in range(len(data)):
                data[i]['1d']['price_change_pct'] = str(float(data[i]['1d']['price_change_pct']) * 100)
                data[i]['7d']['price_change_pct'] = str(float(data[i]['7d']['price_change_pct']) * 100)
            return Response(data)
        else:
            return Response("Brak danych na serwerze")


class CryptocurrencyAllAPI(APIView):
    def get(self, request):
        data = nomics.Currencies.get_currencies(ids="BTC,ETH,ADA,BNB,XRP,SOL,DOT,DOGE,UNI,AVAX,LUNA,LINK,ALGO,LTC,"
                                                    "BCH,ATOM,MATIC",
                                                interval="1d,7d")
        if data:
            for i in range(len(data)):
                data[i]['1d']['price_change_pct'] = str(float(data[i]['1d']['price_change_pct']) * 100)
                data[i]['7d']['price_change_pct'] = str(float(data[i]['7d']['price_change_pct']) * 100)
            return Response(data)
        else:
            return Response("Brak danych na serwerze")


# HTML VIEWS
class Index(View):
    def get(self, request):
        wpisy = Wpis.objects.order_by('-data_utworzenia')[:3]
        context = {
            'wpisy': wpisy,
        }
        return render(request, 'Krypta/index.html', context)

class Dashboard(LoginRequiredMixin,View):
    def get(self, request):
        return render(request,'Krypta/dashboard.html')


class CryptocurrencyList(View):
    def get(self, request):
        return render(request, 'Krypta/kursy.html')


class AktualnosciView(ListView):
    model = Wpis
    ordering = '-data_utworzenia'


class WpisDetail(DetailView):
    model = Wpis


class UserDetail(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'Krypta/user_detail.html')


class CustomLogin(LoginView):
    template_name = 'Krypta/login.html'
    fields = '__all__'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('index')


"""class RegisterPage(FormView):
    template_name = 'Krypta/register.html'
    form_class = UserCreationForm
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        user = form.save()
        if user is not None:
            login(self.request, user)
        return super(RegisterPage, self).form_valid(form)

    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('index')
        return super(RegisterPage, self).get(self, *args, **kwargs)"""

class RegisterPage(View):
    def get(self,request):
        form = UserRegistration()
        context = {
            'form' : form
        }
        return render(request,"Krypta/register.html",context)
    def post(self,request):
        form = UserRegistration(request.POST)
        if form.is_valid():
            user = form.save(commit=True)
            login(request,user)
            return redirect('profil')
        return render(request,'Krypta/register.html',{'form': form})


class EdycjaWpisu(UpdateView):
    template_name = 'Krypta/edycja_wpisu.html'
    model = Wpis
    fields = '__all__'
    success_url = reverse_lazy('aktualnosci')

    def get(self,request,pk):
        if request.user.is_superuser:
            return super(EdycjaWpisu,self).get(self,request,pk)
        else:
            return redirect('index')

class EdycjaProfilu(UpdateView):
    template_name = 'Krypta/edycja_uzytkownika.html'
    model = User
    fields = ('username', 'first_name', 'last_name')
    success_url = reverse_lazy('profil')

    def get(self,request,pk):
        if request.user.id == pk:
            return super(EdycjaProfilu,self).get(self,request,pk)
        return redirect('index')


