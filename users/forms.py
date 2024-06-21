from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.forms import PasswordResetForm, SetPasswordForm
from .models import Profile

class UserLoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control", "id": "username", "placeholder": "Логин или почта"}), label="Логин или почта")
    password = forms.CharField(widget=forms.PasswordInput(attrs={"class": "form-control", "id": "password", "placeholder": "Пароль"}), label="Пароль")
    
class UserRegistrationForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control", "id": "username", "placeholder": "Логин"}), label="Логин")
    email = forms.EmailField(widget=forms.EmailInput(attrs={"class": "form-control", "id": "email", "placeholder": "Ваша почта"}), label="Ваша почта")
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={"class": "form-control", "id": "password1", "placeholder": "Пароль"}), label="Пароль")
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={"class": "form-control", "id": "password2", "placeholder": "Подтверждение пароля"}), label="Подтверждение пароля")
    
    def clean_username(self):
        user_check_username = get_user_model().objects.filter(username=self.cleaned_data["username"])
        if user_check_username:
            raise forms.ValidationError("Пользователь с таким именем уже существует")
        return self.cleaned_data["username"]
                
    def clean_email(self):
        user_check_email = get_user_model().objects.filter(email=self.cleaned_data["email"]) 
        if user_check_email:
            raise forms.ValidationError("Пользователь с такой почтой уже зарегистрирован")
        return self.cleaned_data["email"]

    def clean(self):
        super().clean()
        validate_password(self.cleaned_data["password1"])
        if self.cleaned_data["password1"] != self.cleaned_data["password2"]:
            raise forms.ValidationError("Введенные пароли не совпадают")
        
class UserForm(forms.ModelForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control", "id": "first_name", "placeholder": "Имя"}), label="Имя", required=False)
    last_name = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control", "id": "last_name", "placeholder": "Фамилия"}), label="Фамилия", required=False)
    username = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control", "id": "username", "placeholder": "Логин"}), label="Логин")
    email = forms.EmailField(widget=forms.EmailInput(attrs={"class": "form-control", "id": "email", "placeholder": "Ваша почта"}), label="Ваша почта", disabled=True)
    
    class Meta:
        model = get_user_model()
        fields = ("first_name", "last_name", "username", "email")
    
    
class UserProfileForm(forms.ModelForm):
    avatar = forms.ImageField(widget=forms.FileInput(attrs={"class": "form-control", "id": "avatar", "placeholder": "Фото профиля"}), label="Фото профиля", required=False)
    status = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control", "id": "status", "placeholder": "Статус"}), label="Статус", required=False)
    bio = forms.CharField(widget=forms.Textarea(attrs={"class": "form-control", "id": "bio", "placeholder": "Биография"}), label="Биография", required=False)
    
    class Meta:
        model = Profile
        fields = ("avatar", "status", "bio")
        
    
class UserChangePasswordForm(forms.Form):
    old_password = forms.CharField(widget=forms.PasswordInput(attrs={"class": "form-control", "id": "old_password", "placeholder": "Старый пароль"}), label="Старый пароль")
    new_password1 = forms.CharField(widget=forms.PasswordInput(attrs={"class": "form-control", "id": "new_password1", "placeholder": "Новый пароль"}), label="Новый пароль")
    new_password2 = forms.CharField(widget=forms.PasswordInput(attrs={"class": "form-control", "id": "new_password2", "placeholder": "Подтверждение пароля"}), label="Подтверждение пароля")
    
    def clean(self):
        super().clean()
        validate_password(self.cleaned_data["new_password1"])
        if self.cleaned_data["new_password1"] != self.cleaned_data["new_password2"]:
            raise forms.ValidationError("Введенные новые пароли не совпадают")
        
class UserResetPasswordForm(PasswordResetForm):
    email = forms.EmailField(max_length=254, widget=forms.EmailInput(attrs={"class": "form-control", "id": "email", "placeholder": "Ваша почта"}), label="Ваша почта")
    
    def clean_email(self):
        if not get_user_model().objects.filter(email=self.cleaned_data["email"]).exists():
            raise(forms.ValidationError("Введите корректный email"))
        return self.cleaned_data["email"]
    
class UserConfirmPasswordForm(SetPasswordForm):
    new_password1 = forms.CharField(widget=forms.PasswordInput(attrs={"class": "form-control", "id": "new_password1", "placeholder": "Новый пароль"}), label="Новый пароль")
    new_password2 = forms.CharField(widget=forms.PasswordInput(attrs={"class": "form-control", "id": "new_password2", "placeholder": "Подтверждение пароля"}), label="Подтверждение пароля")