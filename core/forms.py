from django import forms
from django.contrib.auth.models import User
from .models import Project, Issue

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['name', 'description']

class IssueForm(forms.ModelForm):
    class Meta:
        model = Issue
        fields = ['title', 'description', 'status', 'assigned_to']
        widgets = {
            'assigned_to': forms.HiddenInput()  # Hide this field if it's not used actively
        }

class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    password_confirm = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'password')

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("password_confirm")

        if password != confirm_password:
            raise forms.ValidationError("Password and confirm password do not match")
