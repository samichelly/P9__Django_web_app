from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from django.db.models import Value, CharField, Q
from itertools import chain
from .models import Ticket, Review, UserFollows
from .forms import SignUpForm, SignInForm, TicketForm, ReviewForm, SubscriptionForm


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


# à bouger dans les HTML
def get_rating_stars(rating):
    return "★" * rating


@login_required
def home(request):
    following_ids = request.user.following.values_list("followed_user_id", flat=True)

    user_tickets = Ticket.objects.filter(
        Q(user=request.user) | Q(user__id__in=following_ids)
    ).annotate(post_type=Value("ticket", output_field=CharField()))

    user_reviews = Review.objects.filter(
        Q(user=request.user)
        | Q(user__id__in=following_ids)
        | Q(ticket__user=request.user)
    ).annotate(post_type=Value("review", output_field=CharField()))

    for review in user_reviews:
        review.rating = get_rating_stars(review.rating)

    user_posts = sorted(
        chain(user_tickets, user_reviews),
        key=lambda obj: obj.time_created,
        reverse=True,
    )

    return render(request, "home.html", {"user_posts_and_reviews": user_posts})


@login_required
def posts(request):
    user_posts = Ticket.objects.filter(user=request.user).annotate(
        post_type=Value("ticket", output_field=CharField())
    )
    user_reviews = Review.objects.filter(user=request.user).annotate(
        post_type=Value("review", output_field=CharField())
    )

    # Conversion note en étoiles
    for review in user_reviews:
        review.rating = get_rating_stars(review.rating)

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
    print(review)
    print(review.ticket)
    ticket = get_object_or_404(Ticket, id=review.ticket.id)
    print(ticket)

    if request.method == "POST":
        form = ReviewForm(request.POST, instance=review)
        if form.is_valid():
            form.save()
            return redirect("posts")
    else:
        form = ReviewForm(instance=review)

    return render(
        request, "edit_review.html", {"form": form, "review": review, "ticket": ticket}
    )


@login_required
def delete_ticket(request, post_id):
    post = get_object_or_404(Ticket, id=post_id, user=request.user)
    if request.method == "POST":
        post.delete()
        return redirect("posts")
    return render(request, "delete_ticket.html", {"post": post})


@login_required
def delete_review(request, post_id):
    post = get_object_or_404(Review, id=post_id, user=request.user)
    if request.method == "POST":
        post.delete()
        return redirect("posts")
    return render(request, "delete_review.html", {"post": post})


@login_required
def create_review(request, ticket_id=None):
    ticket = None

    if ticket_id:
        ticket = get_object_or_404(Ticket, id=ticket_id)

    # Si ticket existe, créer review simplement
    if request.method == "POST":
        if ticket and ticket.review_exist:
            return render(
                request,
                "create_review.html",
                {"review_exist": True},
            )

        elif ticket:
            form = ReviewForm(request.POST)
            if form.is_valid():
                review = form.save(commit=False)
                review.user = request.user
                review.ticket = ticket
                review.save()
                ticket.review_exist = True
                ticket.save()
                return redirect("home")

        # Sinon créer ticket et review / Modifier la fonction ticket pour l'adapter ?
        else:
            ticket_form = TicketForm(request.POST, request.FILES)
            review_form = ReviewForm(request.POST)
            if ticket_form.is_valid() and review_form.is_valid():
                ticket = ticket_form.save(commit=False)
                ticket.user = request.user
                ticket.review_exist = True
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


@login_required
def profile(request):
    return render(request, "profile.html")


@login_required
def subscription(request):
    already_following = request.user.following.all().values_list(
        "followed_user_id", flat=True
    )

    if request.method == "POST":
        form = SubscriptionForm(
            request.POST,
            users_to_follow=User.objects.exclude(id=request.user.id).exclude(
                id__in=already_following
            ),
        )
        if form.is_valid():
            followed_user = form.cleaned_data["users_to_follow"]
            user_follows = UserFollows(user=request.user, followed_user=followed_user)
            user_follows.save()

            return redirect("subscription")
    else:
        form = SubscriptionForm(
            users_to_follow=User.objects.exclude(id=request.user.id).exclude(
                id__in=already_following
            )
        )

    return render(request, "subscription.html", {"form": form})


@login_required
def unfollow_user(request, user_id_to_unfollow):
    user_to_unfollow = get_object_or_404(User, id=user_id_to_unfollow)

    try:
        user_follows = UserFollows.objects.get(
            user=request.user, followed_user=user_to_unfollow
        )
        user_follows.delete()
    except UserFollows.DoesNotExist:
        pass

    return redirect("subscription")
