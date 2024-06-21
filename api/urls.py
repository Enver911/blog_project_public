from django.urls import path
from api import views


app_name = "api"

urlpatterns = [
    path("tags/", views.PostTag.as_view(), name="PostTag"),
    path("tags/<slug:slug>/", views.PostTagList.as_view(), name="PostTagList"),
    path("posts/", views.PostList.as_view(), name="PostList"),
    path("posts/<slug:slug>/", views.PostDetailed.as_view(), name="PostDetailed"),
    path("posts/<slug:slug>/comments/", views.PostComments.as_view(), name="PostComments"),
    path("posts/<slug:slug>/share", views.PostShare.as_view(), name="PostShare"),
    path("posts/search/<str:keyword>/", views.PostSearch.as_view(), name="PostSearch"),
]

"""
TODO
    path("login/", views.user_login, name="user_login"),
    path("logout/", views.user_logout, name="user_logout"),
    path("registration", views.user_registration, name="user_registration"),
    path("profile/", views.user_profile, name="user_profile"),
    path("password_change/", views.user_password_change, name="user_password_change"),
    path("password_reset/", views.UserPasswordReset.as_view(), name="user_password_reset"),
    path("password_reset/done/", views.user_password_reset_done, name="user_password_reset_done"),
    path("password_reset/<uidb64>/<token>/", views.UserPasswordResetConfirm.as_view(), name="password_reset_confirm"),
"""