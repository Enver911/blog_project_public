from django.http.response import HttpResponse as HttpResponse
from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from .forms import UserLoginForm, UserRegistrationForm, UserForm, UserProfileForm, UserChangePasswordForm, UserResetPasswordForm, UserConfirmPasswordForm
from django.contrib.auth import authenticate, login, logout, get_user_model, update_session_auth_hash
from django.contrib.auth.hashers import make_password
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import PasswordResetView, PasswordResetConfirmView
from django.contrib import messages
from django import forms


# Create your views here.
def user_login(request):
    if request.method == "GET":
        form = UserLoginForm()
        
    elif request.method == "POST":
        form = UserLoginForm(request.POST)
        
        if form.is_valid():    
            # authentication with username or email
            user = authenticate(request, username=form.cleaned_data["username"], password=form.cleaned_data["password"])
            
            # if user was found       
            if user:
                login(request, user)
                # redirect to the page in the "next" param or to the main page
                return HttpResponseRedirect(request.GET.get("next", reverse("blog:post_list")))
             
            form.add_error(field=None, error=forms.ValidationError("Неправильный логин или пароль"))
            
    return render(request, "users/login.html", context={"form": form})
    


#
def user_logout(request):
    logout(request)
    # redirect to the page in the "next" param or to the main page
    return HttpResponseRedirect(request.GET.get("next", reverse("blog:post_list"))) 
 
           
#
def user_registration(request):
    if request.method == "GET":
        form = UserRegistrationForm()
    
    elif request.method == "POST":
        form = UserRegistrationForm(request.POST)
        
        if form.is_valid():  
            get_user_model().objects.create(username=form.cleaned_data["username"], 
                                            email=form.cleaned_data["email"], 
                                            password=make_password(form.cleaned_data["password1"]))
            messages.success(request, "Регистрация прошла успешно!")
            return redirect("users:user_login")  
            
    return render(request, "users/registration.html", context={"form": form})

#
class UserPasswordReset(PasswordResetView):
    email_template_name = "users/password_reset_email.html"
    form_class = UserResetPasswordForm
    template_name = "users/password_reset_form.html"
    success_url = reverse_lazy("users:user_password_reset_done")

def user_password_reset_done(request):
    return render(request, "users/password_reset_done.html")

class UserPasswordResetConfirm(PasswordResetConfirmView):
    form_class = UserConfirmPasswordForm
    template_name = "users/password_reset_confirm.html"
    success_url = reverse_lazy("users:user_login")
     
    def form_valid(self, form):
        messages.success(self.request, message="Пароль был успешно сброшен")
        return super().form_valid(form)
    
    
@login_required(login_url=reverse_lazy("users:user_login"))
def user_profile(request):
    if request.method == "GET":
        profile = UserProfileForm(instance=request.user.profile)
        form = UserForm(instance=request.user)

    elif request.method == "POST":
        profile = UserProfileForm(request.POST, request.FILES, instance=request.user.profile)
        form = UserForm(request.POST, instance=request.user)
        if form.is_valid() and profile.is_valid():
            used_username = get_user_model().objects.filter(username=form.cleaned_data["username"]).exclude(username=request.user.username)
            if not used_username: # if unique username
                form.save()             
                profile.save()                      
                messages.success(request, message="Данные успешно сохранены")
            else:
                form.add_error(field="username", error=forms.ValidationError("Пользователь с таким именем уже существует"))
                        
    return render(request, "users/profile.html", {"profile": profile, "form": form})                
               
               
@login_required(login_url=reverse_lazy("users:user_login"))
def user_password_change(request):
    if request.method == "GET":
        form = UserChangePasswordForm()
    elif request.method == "POST":
        form = UserChangePasswordForm(request.POST)
        if request.user.check_password(request.POST.get("old_password")):
            if form.is_valid():
                request.user.set_password(form.cleaned_data["new_password1"])
                request.user.save()
                update_session_auth_hash(request, request.user)
                messages.success(request, "Пароль успешно изменен!")
                return redirect("users:user_profile")
        else:
            form.add_error(field="old_password", error=forms.ValidationError("Старый пароль введен неверно"))
        
    return render(request, "users/password_change.html", {"form": form})


