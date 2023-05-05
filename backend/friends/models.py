from django.db import models

from users.models import User


class RequestFriend(models.Model):
    from_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='from_user_requests')
    to_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='to_user_requests')
    is_accepted = models.BooleanField(default=False)

    class Meta:
        unique_together = ['from_user', 'to_user']

class Friend(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='friends')
    friends = models.ManyToManyField(User)
