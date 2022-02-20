
from django.urls import path
from contracts import views


urlpatterns = [
    path('deploy/', views.deploy, name='deploy'),
    path('contract_by_address/', views.contract_by_address, name='contract_by_address'),
]
