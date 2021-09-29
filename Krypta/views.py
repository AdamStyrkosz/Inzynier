import requests
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import View, FormView, CreateView, UpdateView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from nomics import Nomics
from .models import Wpis


# Create your views here.

nomics = Nomics('7e9fbd09298ee1d741b02b628020b0bb7a6819e8')

class Index(View):
    def get(self, request):
        data = nomics.Currencies.get_currencies(ids="BTC,ETH,ADA,BNB,XRP,SOL,DOT,LTC",interval="1d,7d")
        if(data):
            wpisy = Wpis.objects.order_by('-data_utworzenia')[:3]
            context = {
                'wpisy': wpisy,
                'crypto_data': data,
            }
            return render(request, 'Krypta/index.html',context)
        else:
            return render(request,'Krypta/brak_danych.html')

class CryptocurrencyList(View):
    def get(self,request):
        data = nomics.Currencies.get_currencies(ids= "BTC,ETH,ADA,BNB,XRP,SOL,DOT,DOGE,UNI,AVAX,LUNA,LINK,ALGO,LTC,"
                                                     "BCH,ATOM,MATIC",
                                                interval="1d,7d")
        context = {'data':data}
        return render(request,'Krypta/kursy.html',context)


class AktualnosciView(ListView):
    model = Wpis
    ordering = '-data_utworzenia'

class WpisDetail(DetailView):
    model = Wpis

class UserDetail(LoginRequiredMixin,View):
    def get(self,request):
        return render(request,'Krypta/user_detail.html')

class CustomLogin(LoginView):
    template_name = 'Krypta/login.html'
    fields = '__all__'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('index')

class RegisterPage(FormView):
    template_name = 'Krypta/register.html'
    form_class = UserCreationForm
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        user = form.save()
        if user is not None:
            login(self.request,user)
        return super(RegisterPage,self).form_valid(form)

    def get(self,*args,**kwargs):
        if self.request.user.is_authenticated:
            return redirect('index')
        return super(RegisterPage,self).get(self,*args,**kwargs)

class EdycjaWpisu(LoginRequiredMixin,UpdateView):
    template_name = 'Krypta/edycja_wpisu.html'
    model = Wpis
    fields = '__all__'
    success_url = reverse_lazy('aktualnosci')



