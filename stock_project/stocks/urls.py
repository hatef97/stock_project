from django.urls import path

from . import views

urlpatterns = [
    path('buy/', views.BuyStockView.as_view()),
]
