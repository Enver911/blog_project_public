from django.urls import path
from . import views


app_name = "blog"

urlpatterns = [
    path("", views.post_list, name="post_list"),
    path("tag/<slug:slug>/", views.post_list, name="post_tag_list"),
    path("search/", views.post_search, name="post_search"),
    path("<slug:slug>/", views.post_detailed, name="post_detailed"),
    path("<slug:slug>/comments/", views.post_comments, name="post_comments"),
    path("<slug:slug>/share/", views.post_share, name="post_share"),
]