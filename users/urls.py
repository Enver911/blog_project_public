from django.urls import path
from django.contrib.auth import views as v
from . import views


app_name = "users"

urlpatterns = [
    
    path("login/", views.user_login, name="user_login"),
    path("logout/", views.user_logout, name="user_logout"),
    path("registration", views.user_registration, name="user_registration"),
    path("profile/", views.user_profile, name="user_profile"),
    path("password_change/", views.user_password_change, name="user_password_change"),
    path("password_reset/", views.UserPasswordReset.as_view(), name="user_password_reset"),
    path("password_reset/done/", views.user_password_reset_done, name="user_password_reset_done"),
    #path("password_reset/<uidb64>/<token>/", v.PasswordResetConfirmView.as_view(), name="password_reset_confirm"),
    path("password_reset/<uidb64>/<token>/", views.UserPasswordResetConfirm.as_view(), name="password_reset_confirm"),

]