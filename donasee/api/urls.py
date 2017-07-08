from django.conf.urls import url

from donasee.api.views import (
    user,
    root,
    campaign,
)

urlpatterns = [
    url(r'^$', root.api_root, name='api-root'),
    url(r'^register/$', user.RegisterView.as_view(), name='register'),
    url(r'^login/$', user.LoginView.as_view(), name='login'),
    url(r'^login-jwt/$', user.LoginJWTView.as_view(), name='login-jwt'),
    url(r'^campaign/$', campaign.CampaignListView.as_view(), name='campaign-list'),
    url(r'^donation/$', campaign.DonationList.as_view(), name='donation-list'),
]
