# from django.contrib.auth.models import User
from django.db import models
from django.contrib.auth.models import User

user_roles = (
    ("admin", "admin"),
    ("staff","staff"),
    ("basic", "basic")
)

class UserModel(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_login = models.BooleanField(default=True)
    role = models.CharField(choices=user_roles, max_length=20)

    def __str__(self):
        return self.user.username
    