
from django.urls import path
from contracts import views


urlpatterns = [
    path('deploy/', views.deploy, name='deploy'),
]
