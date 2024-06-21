from django import forms
from .models import Comment

class EmailPostForm(forms.Form):
    name = forms.CharField(max_length=25, widget=forms.TextInput(attrs={"class": "form-control", "id": "floatingInput", "placeholder": "Ваше имя"}), label="Ваше имя")
    email = forms.EmailField(widget=forms.EmailInput(attrs={"class": "form-control", "id": "floatingEmailSender", "placeholder": "Ваша почта"}), label="Ваша почта")
    to = forms.EmailField(widget=forms.EmailInput(attrs={"class": "form-control", "id": "floatingEmailRecipient", "placeholder": "Почта получателя"}), label="Почта получателя")
    comments = forms.CharField(required=False, widget=forms.Textarea(attrs={"class": "form-control", "id": "floatingCommentsInput", "placeholder": "Комментарий"}), label="Комментарий")

class CommentForm(forms.ModelForm):
    body = forms.CharField(widget=forms.Textarea(attrs={"class": "form-control", "id": "floatingCommentsInput", "placeholder": "Комментарий"}), label="Комментарий")
    class Meta:
        model = Comment
        fields = ["body"]
        
class SearchPostForm(forms.Form):
    query = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control", "id": "query", "placeholder": "Ключевое слово/слова"}), label="Ключевое слово/слова")