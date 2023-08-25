from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django import forms
from .models import Ticket, Review


class SignUpForm(UserCreationForm):
    email = forms.EmailField(
        required=True, help_text="Requis. Veuillez entrer une adresse e-mail valide."
    )

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")


class SignInForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ("username", "password")


class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ("title", "description", "image")


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ("headline", "rating", "body")
