from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils.text import slugify



class Country(models.Model):
    country_name = models.CharField(_('Country Name'), max_length=255)
    code= models.CharField(_('Code'), max_length=255, null=True, blank=True)
    country_code = models.CharField(_('Country Code'),max_length=255, null=True, blank=True)
    created_date = models.DateTimeField(_('Created Date'), auto_now_add=True, editable=False)
    modified_date = models.DateTimeField(_('Modified Date'), auto_now=True, editable=False)



    class Meta:
        ordering = ('country_name',)
        verbose_name = 'country'
        verbose_name_plural = 'countries'

    def __str__(self):
        return '{}'.format(self.country_name)



class State(models.Model):
    country = models.ForeignKey(Country , on_delete=models.CASCADE)
    state_name = models.CharField(_('State Name'), max_length=255)
    state_code = models.CharField(_('State Code'), max_length=255, null=True, blank=True)
    state_type = models.CharField(_('State Type'), max_length=255, null=True, blank=True)

    created_date = models.DateTimeField(_('Created Date'), auto_now_add=True, editable=False)
    modified_date = models.DateTimeField(_('Modified Date'), auto_now=True, editable=False)

    class Meta:
        ordering = ('state_name',)
        verbose_name = 'state'
        verbose_name_plural = 'states'

    def __str__(self):
        return '{}'.format(self.state_name)