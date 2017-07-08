from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.db import models


# Create your models here.
class Campaign(models.Model):
    user = models.ForeignKey(User)
    title = models.CharField(max_length=256)
    money_needed = models.IntegerField()
    description = models.TextField()
    image = models.URLField()

    def __unicode__(self):
        return self.title


class Donation(models.Model):
    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE)
    name = models.CharField(max_length=256)
    amount = models.IntegerField()
    social_security_number = models.CharField(max_length=128)

    def __unicode__(self):
        return self.name + " " + str(self.amount)
