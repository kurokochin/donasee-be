from django.conf.urls import url

from donasee.api.views import (
    user,
    root
)

urlpatterns = [
    url(r'^$', root.api_root, name='api-root'),
    url(r'^register/$', user.RegisterView.as_view(), name='register'),
    url(r'^login/$', user.LoginView.as_view(), name='login'),
]
