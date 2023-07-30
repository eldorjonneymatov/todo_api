from typing import Iterable, Optional
from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _

class Task(models.Model):
    title = models.CharField(_("Title"), max_length=255)
    body = models.TextField(_("Body"))
    is_completed = models.BooleanField(_("Is completed"), default=True)
    created_at = models.DateTimeField(_("Date created"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Last updated"), auto_now=True)
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )


    class Meta:
        ordering = ['is_completed', '-created_at']


    def __str__(self):
        return self.title