import jwt
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models

from users.managers import CustomUserManager
from django.utils.translation import gettext_lazy as _

username_validator = UnicodeUsernameValidator()


class User(AbstractUser):
    email = models.EmailField(_("email address"), unique=True, blank=False, null=False)
    username = models.CharField(
        _("username"),
        max_length=150,
        help_text=_(
            "Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only."
        ),
        validators=[username_validator],
        error_messages={
            "unique": _("A user with that username already exists."),
        },
        blank=True
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email


class RefreshToken(models.Model):
    jti = models.CharField(max_length=255, unique=True)
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    revoked = models.BooleanField(default=False)

    def __str__(self):
        return f"User - {self.user.email} | Token - {self.jti[:10]}... | Is revoked - {self.revoked}"

    @classmethod
    def revoke_all_tokens(cls, user):
        cls.objects.filter(user=user).update(revoked=True)
