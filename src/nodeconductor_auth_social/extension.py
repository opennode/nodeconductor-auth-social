from __future__ import unicode_literals

from nodeconductor.core import NodeConductorExtension


class AuthSocialExtension(NodeConductorExtension):

    class Settings:
        NODECONDUCTOR_AUTH_SOCIAL = {
            'GOOGLE_SECRET': 'CHANGE_ME_TO_GOOGLE_SECRET',
            'FACEBOOK_SECRET': 'CHANGE_ME_TO_FACEBOOK_SECRET',
            'USER_ACTIVATION_URL_TEMPLATE': 'http://example.com/#/activate/{user_uuid}/{token}/',
        }

    @staticmethod
    def django_app():
        return 'nodeconductor_auth_social'

    @staticmethod
    def django_urls():
        from .urls import urlpatterns
        return urlpatterns
