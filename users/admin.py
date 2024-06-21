from django.contrib import admin
from .models import Profile
from django.utils.safestring import mark_safe


# Register your models here.
@admin.register(Profile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ["user", "avatar_image", "status", "bio"]
    search_fields = ["status", "bio"]
    
    fields = ["user", "avatar_image", "avatar", "status", "bio"]
    readonly_fields = ["avatar_image"]
    
    @admin.display(description="Avatar")
    def avatar_image(self, model):
        return mark_safe(f'<p><img class="img-article-left" src="{model.avatar.url}" width="100"></p>' if model.avatar else "Нет фото")
    