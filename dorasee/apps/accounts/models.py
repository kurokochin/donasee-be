# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models


# Create your models here.
class UserProfile(models.Model):
    community_name = models.CharField(max_length=256)
    admin_name = models.CharField(max_length=256)

    STATUS_CHOICES = (
        ('verified', 'verified'),
        ('pending', 'pending')
    )
    status = models.CharField(max_length=8, choices=STATUS_CHOICES)
    docs_link = models.URLField()
