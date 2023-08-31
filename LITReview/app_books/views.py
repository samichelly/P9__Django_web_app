from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from .models import Ticket, Review, UserFollows
from .forms import SignUpForm, SignInForm, TicketForm, ReviewForm
from django.contrib.auth import login, authenticate, logout


from django.db.models import Value, CharField
from django.db.models import F
from itertools import chain


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
    return redirect("signin")


@login_required
def home(request):
    posts = Ticket.objects.all()
    # ajouter les review
    return render(request, "home.html", {"posts": posts})


@login_required
def posts(request):
    user_posts = Ticket.objects.filter(user=request.user).annotate(
        post_type=Value("ticket", output_field=CharField())
    )
    user_reviews = Review.objects.filter(user=request.user).annotate(
        post_type=Value("review", output_field=CharField())
    )

    user_posts_and_reviews = sorted(
        chain(user_posts, user_reviews),
        key=lambda obj: obj.time_created,
        reverse=True,
    )

    return render(
        request, "posts.html", {"user_posts_and_reviews": user_posts_and_reviews}
    )


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


"""
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
"""


@login_required
def edit_ticket(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id, user=request.user)

    if request.method == "POST":
        form = TicketForm(request.POST, request.FILES, instance=ticket)
        if form.is_valid():
            form.save()
            return redirect("posts")
    else:
        form = TicketForm(instance=ticket)

    return render(request, "edit_ticket.html", {"form": form, "ticket": ticket})


@login_required
def edit_review(request, review_id):
    review = get_object_or_404(Review, id=review_id, user=request.user)

    if request.method == "POST":
        form = ReviewForm(request.POST, instance=review)
        if form.is_valid():
            form.save()
            return redirect("posts")
    else:
        form = ReviewForm(instance=review)

    return render(request, "edit_review.html", {"form": form, "review": review})


@login_required
def delete_ticket(request, post_id):
    post = get_object_or_404(Ticket, id=post_id, user=request.user)
    if request.method == "POST":
        post.delete()
        return redirect("posts")
    return render(request, "delete_post.html", {"post": post})


@login_required
def delete_review(request, post_id):
    post = get_object_or_404(Review, id=post_id, user=request.user)
    if request.method == "POST":
        post.delete()
        return redirect("posts")
    return render(request, "delete_post.html", {"post": post})


def subscription(request):
    return render(request, "subscription.html")


@login_required
def create_review(request, ticket_id=None):  # ticket et pas ticket_id
    ticket = None
    if ticket_id:
        ticket = get_object_or_404(Ticket, id=ticket_id)

    # Si ticket existe, créer review simplement
    if request.method == "POST":
        if ticket:
            form = ReviewForm(request.POST)
            if form.is_valid():
                review = form.save(commit=False)
                review.user = request.user
                review.ticket = ticket
                review.save()
                return redirect("home")

        # Sinon créer ticket et review / Modifier la fonction ticket pour l'adapter ?
        else:
            ticket_form = TicketForm(request.POST, request.FILES)
            review_form = ReviewForm(request.POST)
            if ticket_form.is_valid() and review_form.is_valid():
                ticket = ticket_form.save(commit=False)
                ticket.user = request.user
                ticket.save()

                review = review_form.save(commit=False)
                review.user = request.user
                review.ticket = ticket
                review.save()

                return redirect("home")
    else:
        if ticket:
            form = ReviewForm()
            context = {
                "form": form,
                "ticket": ticket,
            }
        else:
            ticket_form = TicketForm()
            review_form = ReviewForm()
            context = {
                "ticket_form": ticket_form,
                "review_form": review_form,
            }

    return render(request, "create_review.html", context)


"""
@login_required
def create_review(request, ticket_id=None):
    ticket = None

    if ticket_id:
        ticket = get_object_or_404(Ticket, id=ticket_id)

    if request.method == "POST":
        review_form = ReviewForm(request.POST)
        if review_form.is_valid():
            review = review_form.save(commit=False)
            review.user = request.user

            if ticket:
                review.ticket = ticket
            else:
                # Créer un ticket vide pour la review
                new_ticket = Ticket.objects.create(user=request.user)
                review.ticket = new_ticket

            review.save()
            return redirect("home")
    else:
        ticket_form = TicketForm()
        review_form = ReviewForm()

    context = {
        "ticket": ticket,
        "ticket_form": ticket_form,
        "review_form": review_form,
    }

    return render(request, "create_review.html", context)

"""

"""
@login_required
def create_review(request, ticket_id=None):
    print(ticket_id)
    ticket = None

    if ticket_id:
        ticket = get_object_or_404(Ticket, id=ticket_id)
        if not ticket.user == request.user:
            raise PermissionDenied("Accès refusé")

    if request.method == "POST":
        review_form = ReviewForm(request.POST)
        if review_form.is_valid():
            review = review_form.save(commit=False)
            review.user = request.user

            if ticket:
                review.ticket = ticket
            else:
                new_ticket = Ticket.objects.create(user=request.user)
                review.ticket = new_ticket

            review.save()
            return redirect("home")
    else:
        ticket_form = TicketForm()
        review_form = ReviewForm()

    context = {
        "ticket": ticket,
        "ticket_form": ticket_form,
        "review_form": review_form,
    }

    return render(request, "create_review.html", context)
"""
