"""
URL configuration for LITReview project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.views.defaults import server_error
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from app_books import views

urlpatterns = [
    path("test_error/", server_error),
    path("admin/", admin.site.urls),
    path("", views.signin, name="signin"),
    path("signup/", views.signup, name="signup"),
    path("home/", views.home, name="home"),
    path("subscription/", views.subscription, name="subscription"),
    path("posts/", views.posts, name="posts"),
    path("create_ticket/", views.create_ticket, name="create_ticket"),
    path("create_review/", views.create_review, name="create_review"),
    path("create_review/<int:ticket_id>/", views.create_review, name="create_review"),
    path("edit_post/<int:post_id>/", views.edit_post, name="edit_post"),
    path("delete_post/<int:post_id>/", views.delete_post, name="delete_post"),
    path('logout/', views.signout, name='logout'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
