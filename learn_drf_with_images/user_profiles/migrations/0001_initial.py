# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import phonenumber_field.modelfields
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date_of_birth', models.DateField(blank=True, verbose_name='date of birth', null=True)),
                ('phone_number', phonenumber_field.modelfields.PhoneNumberField(blank=True, verbose_name='phone number', max_length=128)),
                ('gender', models.CharField(default='U', verbose_name='gender', max_length=1, choices=[('U', 'unknown'), ('M', 'male'), ('F', 'female')])),
                ('image', models.ImageField(blank=True, upload_to='', verbose_name='image', null=True)),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
