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
    username = forms.CharField(
        widget=forms.TextInput(attrs={"placeholder": "Nom d'utilisateur"})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={"placeholder": "Mot de passe"})
    )

    class Meta:
        model = User
        fields = ("username", "password")


class TicketForm(forms.ModelForm):
    title = forms.CharField(
        widget=forms.TextInput(attrs={"placeholder": "Ajouter un titre"})
    )
    description = forms.CharField(
        widget=forms.Textarea(attrs={"placeholder": "Ajouter une description"})
    )
    image = forms.ImageField(label="Sélectionner une image")

    class Meta:
        model = Ticket
        fields = ("title", "description", "image")


class ReviewForm(forms.ModelForm):
    RATING_CHOICES = (
        (0, "0"),
        (1, "1"),
        (2, "2"),
        (3, "3"),
        (4, "4"),
        (5, "5"),
    )

    rating = forms.ChoiceField(choices=RATING_CHOICES, widget=forms.RadioSelect)

    class Meta:
        model = Review
        fields = ["headline", "rating", "body"]


class SubscriptionForm(forms.Form):
    users_to_follow = forms.ModelChoiceField(
        queryset=None,
        widget=forms.Select(attrs={"class": "form-control"}),
    )
    is_following = forms.BooleanField(
        required=False,
        initial=True,
        widget=forms.HiddenInput(),
    )

    users_to_follow.label = ""

    def __init__(self, *args, **kwargs):
        users_to_follow = kwargs.pop("users_to_follow", None)
        super().__init__(*args, **kwargs)
        self.fields["users_to_follow"].queryset = users_to_follow
