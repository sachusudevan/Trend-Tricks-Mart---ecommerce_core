from django.db import models
from django.conf import settings

from django.contrib.auth.models import User
from django.utils.translation import gettext, gettext_lazy as _

class ThemeConfiguration(models.Model):
    THEME = [
        (True, _('dark')),
        (False, _('light')),
    ] 
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    theme = models.BooleanField(_('theme'), default=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user'], name='One Entry Per User')
        ]