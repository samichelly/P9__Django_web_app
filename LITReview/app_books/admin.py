from django.contrib import admin
from .models import Ticket, Review


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "user", "image", "time_created", "review_exist")
    search_fields = ("title", "user__username")
    list_filter = ("user",)


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "ticket",
        "headline",
        "rating",
        "user",
        "time_created",
    )
    search_fields = (
        "headline",
        "user__username",
        "ticket__title",
    )
    list_filter = ("user", "ticket")
