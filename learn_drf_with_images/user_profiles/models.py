from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _

from phonenumber_field.modelfields import PhoneNumberField


class UserProfile(models.Model):
    GENDER_UNKNOWN = 'U'
    GENDER_MALE = 'M'
    GENDER_FEMALE = 'F'
    GENDER_CHOICES = (
        (GENDER_UNKNOWN, _('unknown')),
        (GENDER_MALE, _('male')),
        (GENDER_FEMALE, _('female')),
    )

    user = models.OneToOneField(settings.AUTH_USER_MODEL)
    date_of_birth = models.DateField(_('date of birth'), blank=True, null=True)
    phone_number = PhoneNumberField(_('phone number'), blank=True)
    gender = models.CharField(_('gender'), max_length=1, choices=GENDER_CHOICES, default=GENDER_UNKNOWN)
    image = models.ImageField(_('image'), blank=True, null=True)
