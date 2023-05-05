from django.db import models

from users.models import User


class Request(models.Model):
    from_user = models.ForeignKey(User, on_delete=models.CASCADE)


class Friend(models.Model):
    pass
