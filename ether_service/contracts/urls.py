
from django.urls import path
from contracts import views


urlpatterns = [
    path('deploy/', views.deploy, name='deploy'),
    path('contract_by_address/', views.contract_by_address, name='contract_by_address'),
    path('contracts_by_owner/', views.contracts_by_owner, name='contract_by_address'),
    path('load_contract/', views.load_contract_and_set_to_cache, name='load contract and set to cache'),
    path('start/', views.start_ether_service, name='start ether service'),
]
