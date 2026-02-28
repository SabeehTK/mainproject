from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from accounts.models import Profile

from accounts.models import EmailOTP


class UserForm(UserCreationForm):
    rolechoices = [
        ('buyer', 'Buyer'),
        ('agent', 'Agent'),
    ]
    role = forms.ChoiceField(choices=rolechoices)
    class Meta():
        model = User
        fields = ['username', 'email', 'password1', 'password2','first_name','last_name','role']

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
            role = self.cleaned_data['role']
            # Update or create profile with role
            Profile.objects.update_or_create(user=user, defaults={'role': role})
        return user

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        exclude = ['user','role']
class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

class OtpLoginForm(forms.ModelForm):
    class Meta:
        model = EmailOTP
        fields = ['user']