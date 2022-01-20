
from django.urls import path
from ether_network import views


urlpatterns = [
    path('connect/', views.connect, name='connect'),
    path('disconnect/', views.disconnect, name='disconnect'),
    path('gas_limit/', views.gas_limit, name='gas_limit'),
    path('gas_price/', views.gas_price, name='gas_price'),
    path('is_connected/', views.is_connected, name='is_connected'),
    path('show_active/', views.show_active, name='show_active'),
]
