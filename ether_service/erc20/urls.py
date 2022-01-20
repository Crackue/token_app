
from django.urls import path
from erc20 import views


urlpatterns = [
    path('name/', views.name, name='name'),
    path('symbol/', views.symbol, name='symbol'),
    path('decimals/', views.decimals, name='decimals'),
    path('total_supply/', views.total_supply, name='total_supply'),
    path('balance_of/', views.balance_of, name='balance_of'),
    path('transfer/', views.transfer, name='transfer'),
    path('transfer_from/', views.transfer_from, name='transfer_from'),
    path('approve/', views.approve, name='approve'),
    path('allowance/', views.allowance, name='allowance'),
]
