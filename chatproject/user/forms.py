from django import forms
from django.contrib.auth.models import User
from .models import Profile

class UserEditform(forms.ModelForm):

    class Meta:
        model = User
        fields = {'email', 'first_name', 'last_name'}


class ProfileEditform(forms.ModelForm):

    class Meta:
        model = Profile
        fields = {'decs', 'photo'}


class RegistrationForm(forms.ModelForm):

    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = {'username', 'email', 'first_name'}
    
    def check_password(self):
        if self.cleaned_data['password'] != self.cleaned_data['password2']:
            raise forms.ValidationError('Passwords do not math')
        
        return self.cleaned_data['password2']