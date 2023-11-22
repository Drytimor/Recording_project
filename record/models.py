from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser
from django.db.models import F, Q
# Create your models here.


class User(AbstractUser):
    pass


