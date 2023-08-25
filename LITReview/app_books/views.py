from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from .models import Ticket, Review, UserFollows
from .forms import SignUpForm, SignInForm, TicketForm, ReviewForm
from django.contrib.auth import login, authenticate, logout


def signup(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("signin")
    else:
        form = SignUpForm()
    return render(request, "signup.html", {"form": form})


def signin(request):
    if request.method == "POST":
        form = SignInForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect("home")
    else:
        form = SignInForm(request)
    return render(request, "signin.html", {"form": form})


@login_required
def signout(request):
    logout(request)
    return redirect("home")


@login_required
def home(request):
    following_users = request.user.following.all()
    following_users_ids = [user.id for user in following_users]
    posts = Ticket.objects.filter(user__in=following_users_ids) | Ticket.objects.filter(
        user=request.user
    )
    return render(request, "home.html", {"posts": posts})


@login_required
def create_ticket(request):
    if request.method == "POST":
        form = TicketForm(request.POST, request.FILES)
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.user = request.user
            ticket.save()
            return redirect("posts")
    else:
        form = TicketForm()
    return render(request, "create_ticket.html", {"form": form})


@login_required
def edit_post(request, post_id):
    post = get_object_or_404(Ticket, id=post_id, user=request.user)
    if request.method == "POST":
        form = TicketForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            return redirect("posts")
    else:
        form = TicketForm(instance=post)
    return render(request, "edit_post.html", {"form": form, "post": post})


@login_required
def delete_post(request, post_id):
    post = get_object_or_404(Ticket, id=post_id, user=request.user)
    if request.method == "POST":
        post.delete()
        return redirect("posts")
    return render(request, "delete_post.html", {"post": post})


@login_required
def posts(request):
    user_posts = Ticket.objects.filter(user=request.user)
    return render(request, "posts.html", {"user_posts": user_posts})


@login_required
def create_review(request, post_id):
    ticket = get_object_or_404(Ticket, id=post_id)
    if request.method == "POST":
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.ticket = ticket
            review.save()
            return redirect("posts")
    else:
        form = ReviewForm()
    return render(request, "create_review.html", {"form": form, "ticket": ticket})


def subscription(request):
    return render(request, "subscription.html")
