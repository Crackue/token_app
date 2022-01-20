from django.urls import path
from user_service_app import views


urlpatterns = [
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('signin/', views.signin, name='signin'),
    path('is_logged_in/', views.is_logged_in, name='is_logged_in'),
    path('get_user_by_name/', views.get_user_address_by_name, name='get_user_address_by_name'),
]
