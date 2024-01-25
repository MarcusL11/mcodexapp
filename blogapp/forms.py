from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User 
from django import forms
from . models import Subscriber
class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1','password2']

class UserLoginForm(forms.Form):
    username = forms.CharField(max_length=100)
    password = forms.CharField(max_length=100, widget=forms.PasswordInput)


class SubscriberForm(forms.ModelForm):
    class Meta:
        model = Subscriber
        fields = ['subscribe']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['subscribe'].label = "Subscribe to emails"
        self.fields['subscribe'].required = False

class UpdateProfilePicForm(forms.ModelForm):
    profile_pic = forms.ImageField(widget=forms.FileInput(attrs={'class': 'form-control-file'}))
    class Meta:
        model = Subscriber
        fields = ['profile_pic']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['profile_pic'].label = "Profie Picture"
        self.fields['profile_pic'].required = False