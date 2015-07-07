# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0006_require_contenttypes_0002'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('user', models.OneToOneField(primary_key=True, to=settings.AUTH_USER_MODEL, serialize=False)),
                ('date_of_birth', models.DateField(verbose_name='date of birth', blank=True, null=True)),
                ('phone_number', phonenumber_field.modelfields.PhoneNumberField(verbose_name='phone number', blank=True, max_length=128)),
                ('gender', models.CharField(choices=[('U', 'unknown'), ('M', 'male'), ('F', 'female')], default='U', verbose_name='gender', max_length=1)),
                ('image', models.ImageField(upload_to='', verbose_name='image', blank=True, null=True)),
            ],
        ),
    ]
