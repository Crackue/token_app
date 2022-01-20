from django.urls import path
from ether_accounts import views


urlpatterns = [
    path('add/', views.add, name='add'),
    path('at/', views.at, name='at'),
    path('connect_to_clef/', views.connect_to_clef, name='connect_to_clef'),
    path('disconnect_from_clef/', views.disconnect_from_clef, name='disconnect_from_clef'),
    path('from_mnemonic/', views.from_mnemonic, name='from_mnemonic'),
    path('load/', views.load, name='load'),
    path('remove/<str:address>', views.remove, name='remove'),
    path('clear/', views.clear, name='clear'),
    path('is_local_account/', views.is_local_account, name='is_local_account'),
]
