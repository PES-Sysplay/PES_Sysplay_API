from django.urls import path

from chat.views import ChatView, ChatIndividualView

urlpatterns = [
    path('', ChatView.as_view(), name='chat'),
    path('<int:id>/', ChatIndividualView.as_view(), name='chat_individual'),
]
