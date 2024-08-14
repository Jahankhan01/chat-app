from django.urls import path, include
from chat import views as chat_views
from django.contrib.auth.views import LoginView, LogoutView
from chat.views import RegisterView
from .views import ConversationListView, ConversationDetailView, JoinConversationView, SendMessageView
from .views import ConversationCreateView



urlpatterns = [
    # path("", chat_views.chatPage, name="chat-page"),
    path("auth/login/", LoginView.as_view(template_name="chat/loginPage.html"), name="login-user"),
    path("auth/logout/", LogoutView.as_view(), name="logout-user"),
    path('register/', RegisterView.as_view(), name='register'),

    path('', ConversationListView.as_view(), name='conversation_list'),
    path('conversation/<uuid:pk>/', ConversationDetailView.as_view(), name='conversation_detail'),
    path('join/', JoinConversationView.as_view(), name='join_conversation'),
    path('conversation/<uuid:pk>/send/', SendMessageView.as_view(), name='send_message'),
    path('conversations/new/', ConversationCreateView.as_view(), name='conversation_create'),
]