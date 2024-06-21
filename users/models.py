from django.db import models
from django.contrib.auth import get_user_model
from PIL import Image


# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE, related_name="profile")
    avatar = models.ImageField(default="default.png", upload_to="profile_images")
    status = models.TextField(max_length=100, blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return self.user.get_username()
    
    class Meta:
        verbose_name = "Профиль"
        verbose_name_plural = "Профили"
        
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        
        image = Image.open(self.avatar.path)
        if image.height > 400 or image.width > 400:
            image.thumbnail((400, 400))
            image.save(self.avatar.path)