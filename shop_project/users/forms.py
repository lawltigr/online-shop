from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from .models import Profile

class RegisterForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter email'})
    )
    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'password1',
            'password2'
        ]
    def __init__(self, *args, **kwargs):
        super().__init__(*args, *kwargs)
        self.fields['username'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Enter username'
        })
        self.fields['password1'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Enter password'
        })
        self.fields['password2'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Repeat password'
        })

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model=User
        fields = ['username', 'email']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }

class ProfileUpdateForm(forms.ModelForm):
    class Meta: 
        model=Profile
        fields=['avatar', 'phone', 'address']
        widgets={
            'avatar':forms.FileInput(attra={'class': 'form-control'}),
            'phone':forms.TextInput(attra={'class': 'form-control', 'placeholder': '+7 777 777 77 77'}),
            'address':forms.Textarea(attra={'class': 'form-control', 'placeholder': 'Delivery address', 'rows': 3}),
        }