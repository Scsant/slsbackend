from django.urls import path
from .views import ChatView, HistoryView

urlpatterns = [
    path('chat/', ChatView.as_view(), name='chat'),
    path('history/', HistoryView.as_view(), name='history'),
]

