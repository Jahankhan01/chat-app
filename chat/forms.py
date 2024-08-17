from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Conversation

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class JoinConversationForm(forms.Form):
    conversation = forms.ModelChoiceField(
        queryset=Conversation.objects.all(),
        label="Select a Conversation",
        required=True
    )

class ConversationForm(forms.Form):
    name = forms.CharField(
        max_length=255,
        label="Conversation Name",
        widget=forms.TextInput(attrs={'placeholder': 'Enter the conversation name'}),
        required=True
    )
    users = forms.ModelMultipleChoiceField(
        queryset=User.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=True,
        label="Select users to add to the conversation"
    )

    def __init__(self, *args, **kwargs):
        logged_in_user = kwargs.pop('logged_in_user', None)
        super().__init__(*args, **kwargs)
        if logged_in_user:
            self.fields['users'].queryset = User.objects.exclude(id=logged_in_user.id)