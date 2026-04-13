from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.core.mail import send_mail
from django.utils.translation import gettext_lazy as _
from django_stubs_ext.db.models import TypedModelMeta

from .managers import CustomUserManager


class BaseUserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name=_("profile"))
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    avatar = models.ImageField(upload_to='users/%Y/%m/%d', blank=True, null=True)
    date_of_birth = models.IntegerField(blank=True, null=True)
    theme = models.CharField(max_length=20, default="light")
    language = models.CharField(max_length=10, default="fr")

    class Meta:
        abstract = True
        verbose_name_plural = "users profil"  

    def __str__(self) -> str:
        return f'Profile de {self.user.trigram}'

class MyUser(AbstractUser):

    class UserTypes(models.TextChoices):
        MEMBER = "member", "Member"
        SUPERMEMBER = "supermember", "Supermember"

    first_name = None
    last_name = None
    username = None
    email = models.EmailField(_("email address"), unique=True, max_length=50)
    trigram = models.CharField(max_length=5, blank=False)
    usertype = models.CharField(
        max_length=30, choices=UserTypes.choices, default=UserTypes.MEMBER, blank=True
    )

    last_password_change = models.DateTimeField(
        _("Dernier changement de mot de passe"), null=True, blank=True
    )
    last_email_change = models.DateTimeField(
        _("Dernier changement d'email"), null=True, blank=True
    )
    last_trigram_change = models.DateTimeField(
        _("Dernier changement de trigram"), null=True, blank=True
    )

    stopwatch = models.BooleanField(default=False)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["trigram"]

    groups = models.ManyToManyField(
        Group,
        verbose_name='groups',
        blank=True,
        help_text=_('Les groupes auxquels appartient l\'utilisateur'),
        related_name="myuser_set",  
    )

    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name='user permissions',
        blank=True,
        help_text=_('Les permissions de l\'utilisateur'),
        related_name="myuser_permission_set",
    )

    objects = CustomUserManager()

    def __str__(self):
        return f"{self.trigram}"

    def can_modify_apps(self):
        """Permet de savoir si l'utilisateur a les droits pour modifier les apps"""
        return self.usertype == self.UserTypes.SUPERMEMBER or self.is_staff

    def request_app_modification(self, requested_apps):
        """Envoie un mail à l'administrateur pour demander la modification des apps"""

        subject = f"Demande de modification d'applications pour {self.trigram}"
        message = f"""
        L'utilisateur {self.trigram} ({self.email})
        a demandé une modification de ses applications autorisées.
        Applications demandées : {', '.join(requested_apps)}

        Veuillez traiter cette demande via l'interface d'administration.
        """

        send_mail(
            subject,
            message,
            self.email,
            [settings.ADMIN_EMAIL],
            fail_silently=False,
        )

    class Meta(TypedModelMeta):
        verbose_name_plural = "users"
        verbose_name = "user"
        ordering = ["-trigram"]
        indexes = [
            models.Index(fields=["-trigram"]),
        ]

class MemberProfile(BaseUserProfile):
    """specific data to member"""

    def get_avatar_url(self):
        if self.avatar:
            return self.avatar.url
        return "/theme/static/images/secret.jpeg"  # Chemin vers l'avatar par défaut

class MemberManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(usertype=CQUser.UserTypes.MEMBER)

    def get_by_natural_key(self, email):
        return self.get(email=email)

class Member(MyUser):

    class Meta(TypedModelMeta):
        proxy = True

    objects = MemberManager()

    @property
    def profile(self):
        try:
            return self._profile
        except MemberProfile.DoesNotExist:
            return MemberProfile.objects.create(
                user=self,
            )