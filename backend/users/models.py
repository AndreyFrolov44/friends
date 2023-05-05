from django.db import models
from django.contrib.auth.models import PermissionsMixin, AbstractBaseUser

from .managers import UserManager


class User(AbstractBaseUser, PermissionsMixin):
    id = models.AutoField(primary_key=True, unique=True) 
    username = models.CharField(max_length=50, unique=True) 
    is_active = models.BooleanField(default=True) 
    is_staff = models.BooleanField(default=False) 
    
    USERNAME_FIELD = 'username'

    objects =  UserManager()
 