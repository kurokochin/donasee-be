# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

# Register your models here.
from donasee.apps.campaign.models import Campaign, Donation


class CampaignAdmin(admin.ModelAdmin):
    pass


class DonationAdmin(admin.ModelAdmin):
    pass


admin.site.register(Campaign, CampaignAdmin)
admin.site.register(Donation, DonationAdmin)
