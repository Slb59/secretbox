from django.db import models
from django.conf import settings  

class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="profile")
    photo = models.ImageField(upload_to='users/%Y/%m/%d', blank=True, null=True)
    date_of_birth = models.IntegerField(blank=True, null=True)
    theme = models.CharField(max_length=20, default="light")
    language = models.CharField(max_length=10, default="fr")

    class Meta:
        verbose_name_plural = "users profil"  

    def __str__(self) -> str:
        return f'Profile de {self.user.username}'

