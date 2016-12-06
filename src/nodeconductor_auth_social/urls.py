from __future__ import unicode_literals

from django.conf.urls import patterns, url

from . import views

urlpatterns = patterns(
    '',
    url(r'^api-auth/google/$', views.GoogleView.as_view(), name='auth_google'),
    url(r'^api-auth/facebook/$', views.FacebookView.as_view(), name='auth_facebook'),
    url(r'^api-auth/registration/$', views.RegistrationView.as_view()),
    url(r'^api-auth/activation/$', views.ActivationView.as_view()),
)
