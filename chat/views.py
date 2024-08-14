from django.shortcuts import render, redirect
from django.views.generic import CreateView
from django.contrib.auth.models import User
from .forms import RegisterForm, JoinConversationForm
from django.urls import reverse_lazy
from django.views.generic import ListView
from django.views.generic import DetailView
from .models import Conversation, ConversationMessage
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import FormView
from django.views.generic.edit import CreateView
from .forms import ConversationForm
from django.views import View


def chatPage(request, *args, **kwargs):
    if not request.user.is_authenticated:
        return redirect("login-user")
    context = {}
    return render(request, "chat/chatPage.html", context)

class RegisterView(CreateView):
    model = User
    form_class = RegisterForm
    template_name = 'chat/register.html'
    success_url = reverse_lazy('login-user')


class ConversationListView(LoginRequiredMixin, ListView):
    model = Conversation
    template_name = 'chat/conversation_list.html'  # Use the template name from the previous example
    context_object_name = 'conversations'

    def get_queryset(self):
        return Conversation.objects.filter(users=self.request.user)


class ConversationDetailView(LoginRequiredMixin, DetailView):
    model = Conversation
    template_name = 'chat/conversation_detail.html'
    context_object_name = 'conversation'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['messages'] = ConversationMessage.objects.filter(conversation=self.object)
        return context


class JoinConversationView(LoginRequiredMixin, View):
    form_class = JoinConversationForm
    template_name = 'chat/join_conversation.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            conversation = form.cleaned_data['conversation']
            conversation.users.add(request.user)  # Add the current user to the selected conversation
            return redirect('conversation_detail', pk=conversation.pk)
        return render(request, self.template_name, {'form': form})


class SendMessageView(LoginRequiredMixin, CreateView):
    model = ConversationMessage
    fields = ['message', 'attachment', 'tagged_message']
    template_name = 'chat/send_message.html'

    def form_valid(self, form):
        form.instance.users = self.request.user
        form.instance.conversation = Conversation.objects.get(pk=self.kwargs['pk'])
        self.object = form.save()
        # Handle notification logic here (e.g., via Django Channels)
        return super().form_valid(form)

    def get_success_url(self):
        return self.object.conversation.get_absolute_url()

class ConversationCreateView(LoginRequiredMixin, FormView):
    template_name = 'chat/conversation_form.html'
    form_class = ConversationForm
    success_url = reverse_lazy('conversation_list')  # Change to your conversation list URL

    def form_valid(self, form):
        # Extract conversation name and selected users from the form
        conversation_name = form.cleaned_data['name']
        selected_users = form.cleaned_data['users']

        # Create a new conversation with the provided name
        conversation = Conversation.objects.create(name=conversation_name)

        # Add the selected users to the conversation
        conversation.users.set(selected_users)
        conversation.users.add(self.request.user)  # Add the current user to the conversation as well

        # Redirect to the new conversation's detail page
        self.success_url = reverse_lazy('conversation_detail', kwargs={'pk': conversation.pk})
        
        return super().form_valid(form)