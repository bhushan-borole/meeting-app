from django.contrib.auth.models import User
from django.db import models


class Meta:
    model = User
    fields = ("username",)
