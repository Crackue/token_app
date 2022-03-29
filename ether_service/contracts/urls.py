
from django.urls import path
from contracts import views


urlpatterns = [
    path('deploy/', views.deploy, name='deploy'),
    path('contract_by_address/', views.contract_by_address, name='contract_by_address'),
    path('load_contract/', views.load_contract_and_set_to_cache, name='load contract and set to cache'),
]
