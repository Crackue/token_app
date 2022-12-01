
from django.urls import path
from ether_project import views


urlpatterns = [
    path('compile_source/', views.compile_source, name='compile_source'),
    path('from_brownie_mix/', views.from_brownie_mix, name='from_brownie_mix'),
    path('from_ethpm/', views.from_ethpm, name='from_ethpm'),
    path('load/', views.load, name='load'),
    path('new/', views.new, name='new'),
    path('run/', views.run, name='run'),
]
