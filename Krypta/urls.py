from django.contrib.auth.views import LogoutView
from django.urls import path

from . import views

urlpatterns = [
    path('', views.Index.as_view(),name = 'index'),
    path('aktualnosci/<int:pk>',views.WpisDetail.as_view(),name='wpis'),
    path('profil',views.UserDetail.as_view(),name='profil'),
    path('wyloguj',LogoutView.as_view(next_page='index'),name='wyloguj'),
    path('aktualnosci',views.AktualnosciView.as_view(),name='aktualnosci'),
    path('login',views.CustomLogin.as_view(),name='login'),
    path('rejestracja',views.RegisterPage.as_view(),name='register'),
    path('kursy',views.CryptocurrencyList.as_view(),name='kursy'),
]