from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid

from .managers import CustomUserManager

class AccountStatus(models.TextChoices):
    ACTIVE = 'ACT'
    BLOCKED = 'BLO'
    COMPROMISED = 'COM'
    CLOSED = 'CLO'
    UNKOWN = 'UNK'

class CustomUser(AbstractUser):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    email = models.EmailField(max_length=255, unique=True)

    username = models.CharField(max_length=255, blank=True)
    phone = models.CharField(max_length=15, blank=True)
    
    balance = models.DecimalField(default=0.0, max_digits=30, decimal_places=4)
    is_seller = models.BooleanField(default=False)
    status = models.CharField(max_length=10, choices=AccountStatus.choices, default=AccountStatus.ACTIVE)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateField(auto_now=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['phone'] # should exclude USERNAME_FIELD & password
    objects = CustomUserManager()

    def __str__(self):
        return self.email