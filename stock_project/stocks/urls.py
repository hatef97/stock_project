from django.urls import path

from . import views

urlpatterns = [
    path('', views.BuyStock.as_view()),
]
