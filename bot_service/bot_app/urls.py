from django.urls import path
from bot_app import views
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path('start/', views.start_bot, name='start_bot'),
    path('webhook_post/', csrf_exempt(views.TelegramBotWebhookView.as_view()), name='post'),
]