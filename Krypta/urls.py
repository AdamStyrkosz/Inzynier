from django.contrib.auth.views import LogoutView
from django.urls import path, include
from rest_framework import routers
from rest_framework.routers import SimpleRouter

from . import views
from .views import CryptocurrencyDetailView

router = SimpleRouter()
#router.register('cryptocurrency',CryptocurrencyViewSet,'cryptocurrency')


urlpatterns = [
    path('', views.Index.as_view(),name = 'index'),
    path('aktualnosci/<int:pk>',views.WpisDetail.as_view(),name='wpis'),
    path('profil',views.UserDetail.as_view(),name='profil'),
    path('wyloguj',LogoutView.as_view(next_page='index'),name='wyloguj'),
    path('aktualnosci',views.AktualnosciView.as_view(),name='aktualnosci'),
    path('login',views.CustomLogin.as_view(),name='login'),
    path('rejestracja',views.RegisterPage.as_view(),name='register'),
    path('kursy',views.CryptocurrencyList.as_view(),name='kursy'),
    path('edycja_wpisu/<int:pk>',views.EdycjaWpisu.as_view(),name='edycja_wpisu'),
    path('edycja_profilu/<int:pk>', views.EdycjaProfilu.as_view(), name='edycja_profilu'),
    path('dashboard',views.Dashboard.as_view(),name='dashboard'),
    path('kryptowaluta/<str:id>',views.CryptoDetail.as_view(),name='crypto_detail'),



    #API URL
    path('cryptocurrencyIndexAPI',views.CryptocurrencyIndexAPI.as_view(),name='cryptoindexapi'),
    path('cryptocurrencyAllAPI',views.CryptocurrencyAllAPI.as_view(),name='cryptoallapi'),
    path('cryptocurrencyDetail/<str:id>',views.CryptocurrencyDetailView.as_view(),name='cryptocurrencydetail')
]

#urlpatterns+= router.urls