from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.models import User
from .forms import SignUpForm, SignInForm, TicketForm, ReviewForm, SubscriptionForm
from .models import Ticket, Review, UserFollows

from django.contrib.auth.decorators import login_required


def signup(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("signin")
    else:
        # est déclenché au premier affichage,
        # requete GET avec form vide. une fois submit, requete POST dclenché
        form = SignUpForm()
        # return redirect("test_connexion")
    return render(request, "signup.html", {"form": form})


def signin(request):
    if request.method == "POST":
        form = SignInForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect("home")
    else:
        form = SignInForm()  # à voir la diff avec POST
    return render(request, "signin.html", {"form": form})


def user_logout(request):
    logout(request)
    return redirect("signin")


@login_required
def home(request):
    if request.user.is_authenticated:
        following_users = request.user.following.all()
        following_users_ids = [user.id for user in following_users]
        posts = Ticket.objects.filter(
            user__in=following_users_ids
        ) | Ticket.objects.filter(user=request.user)
    else:
        posts = Ticket.objects.all()

    return render(request, "home.html", {"posts": posts})


def subscription(request):
    if request.method == "POST":
        form = SubscriptionForm(
            request.POST, users_to_follow=User.objects.exclude(id=request.user.id)
        )
        if form.is_valid():
            followed_user = form.cleaned_data["users_to_follow"]
            user_follows = UserFollows(user=request.user, followed_user=followed_user)
            user_follows.save()
            return redirect("subscription")
    else:
        form = SubscriptionForm(
            users_to_follow=User.objects.exclude(id=request.user.id)
        )
    return render(request, "subscription.html", {"form": form})


# @login_required
def create_ticket(request):
    if request.method == "POST":
        form = TicketForm(request.POST, request.FILES)
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.author = request.user
            form.save()
            return redirect("posts")
    else:
        form = TicketForm()
    return render(request, "create_ticket.html", {"form": form})


# @login_required  # Assurez-vous que l'utilisateur est connecté pour accéder à cette vue
def create_review(request):
    if request.method == "POST":
        form = ReviewForm(request.POST)
        if form.is_valid():
            # billet = form.save(commit=False)
            # billet.author = request.user
            form.save()
            return redirect(
                "home"
            )  # Redirigez vers la page d'accueil après la création du billet
    else:
        form = ReviewForm()
    return render(request, "create_review.html", {"form": form})


@login_required
def posts(request):
    user_posts = Ticket.objects.filter(user=request.user)
    return render(request, "posts.html", {"user_posts": user_posts})
