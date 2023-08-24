from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django import forms
from .models import Ticket, Review


class SignUpForm(UserCreationForm):
    # Ajouter des champs personnalisés
    # utiliser directemet cet import forms.ModelForm ?
    class Meta:
        model = User
        fields = ("username", "password1", "password2")


class SignInForm(AuthenticationForm):
    # Ajouter des champs personnalisés
    # utiliser directemet cet import forms.ModelForm ?
    class Meta:
        model = User
        fields = ("username", "password")


class SubscriptionForm(forms.Form):
    users_to_follow = forms.ModelChoiceField(
        queryset=None,
        widget=forms.Select(attrs={"class": "form-control"}),
    )

    def __init__(self, *args, **kwargs):
        users_to_follow = kwargs.pop("users_to_follow", None)
        super().__init__(*args, **kwargs)
        self.fields["users_to_follow"].queryset = users_to_follow



class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ("title", "description", "user")  # , "image")


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ("headline", "rating", "body")
