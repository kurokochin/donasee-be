# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.db import models


# Create your models here.
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    community_name = models.CharField(max_length=256)
    admin_name = models.CharField(max_length=256)

    STATUS_CHOICES = (
        ('verified', 'verified'),
        ('pending', 'pending')
    )
    status = models.CharField(max_length=8, choices=STATUS_CHOICES, default='pending')
    docs_link = models.URLField()
    error_message = models.CharField(null=True, blank=True, max_length=512)
