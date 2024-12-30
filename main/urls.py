from django.urls import path
from .views import SendMessageView, ReceivedMessagesView

urlpatterns = [
    path('send/<str:link>/', SendMessageView.as_view(), name='send_message'),
    path('received/', ReceivedMessagesView.as_view(), name='received_messages'),
]
