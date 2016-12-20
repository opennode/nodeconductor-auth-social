import json
import os
import random
import requests
import string
import uuid

from urlparse import parse_qsl

from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import transaction, IntegrityError
from rest_framework import views, status, response, generics
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import ValidationError

from nodeconductor.core.views import RefreshTokenMixin

from . import tasks
from .models import AuthProfile
from .serializers import RegistrationSerializer, ActivationSerializer, AuthSerializer


auth_social_settings = getattr(settings, 'NODECONDUCTOR_AUTH_SOCIAL', {})
GOOGLE_SECRET = auth_social_settings.get('GOOGLE_SECRET')
FACEBOOK_SECRET = auth_social_settings.get('FACEBOOK_SECRET')


class AuthException(Exception):
    pass


class FacebookException(AuthException):
    def __init__(self, facebook_error):
        self.message_text = facebook_error.get('message', 'Undefined')
        self.message_type = facebook_error.get('type', 'Undefined')
        self.message_code = facebook_error.get('code', 'Undefined')
        self.message = 'Facebook error {} (code:{}): {}'.format(self.message_type, self.message_code, self.message_text)

    def __str__(self):
        return self.message


class GoogleException(AuthException):
    def __init__(self, google_error):
        self.message_text = google_error.get('message', 'Undefined')
        self.message_code = google_error.get('code', 'Undefined')
        self.message = 'Google error (code:{}): {}'.format(self.message_code, self.message_text)

    def __str__(self):
        return self.message


def generate_password(length=10):
    chars = string.ascii_letters + string.digits + '!@#$%^&*()'
    random.seed = (os.urandom(1024))

    return ''.join(random.choice(chars) for i in range(length))


def generate_username(name):
    return uuid.uuid4().hex[:30]


class BaseAuthView(RefreshTokenMixin, views.APIView):
    permission_classes = []
    authentication_classes = []
    provider = None  # either 'google' or 'facebook'

    def post(self, request, format=None):
        if not self.request.user.is_anonymous():
            raise ValidationError('This view is for anonymous users only.')

        serializer = AuthSerializer(data={
            'client_id': request.data.get('clientId'),
            'redirect_uri': request.data.get('redirectUri'),
            'code': request.data.get('code')
        })
        serializer.is_valid(raise_exception=True)

        backend_user = self.get_backend_user(serializer.validated_data)
        user, created = self.create_or_update_user(backend_user['id'], backend_user['name'])

        token = self.refresh_token(user)

        return response.Response({'token': token.key},
                                 status=created and status.HTTP_201_CREATED or status.HTTP_200_OK)

    def get_backend_user(self, validated_data):
        """
        It should return dictionary with fields 'name' and 'id'
        """
        raise NotImplementedError

    def create_or_update_user(self, user_id, user_name):
        try:
            with transaction.atomic():
                user = get_user_model().objects.create_user(
                    username=generate_username(user_name),
                    password=generate_password(),
                    full_name=user_name,
                    registration_method=self.provider
                )
                setattr(user.auth_profile, self.provider, user_id)
                user.auth_profile.save()
                return user, True
        except IntegrityError:
            profile = AuthProfile.objects.get(**{self.provider: user_id})
            if profile.user.full_name != user_name:
                profile.user.full_name = user_name
                profile.user.save()
            return profile.user, False


class GoogleView(BaseAuthView):

    provider = 'google'

    def get_backend_user(self, validated_data):
        access_token_url = 'https://www.googleapis.com/oauth2/v3/token'
        people_api_url = 'https://www.googleapis.com/plus/v1/people/me/openIdConnect'

        payload = dict(client_id=validated_data['client_id'],
                       redirect_uri=validated_data['redirect_uri'],
                       client_secret=GOOGLE_SECRET,
                       code=validated_data['code'],
                       grant_type='authorization_code')

        # Step 1. Exchange authorization code for access token.
        r = requests.post(access_token_url, data=payload)

        token = json.loads(r.text)
        headers = {'Authorization': 'Bearer {0}'.format(token['access_token'])}

        # Step 2. Retrieve information about the current user.
        r = requests.get(people_api_url, headers=headers)
        response_data = json.loads(r.text)

        # Step 3. Check is response valid.
        if 'error' in response_data:
            raise GoogleException(response_data['error'])

        return {
            'id': response_data['sub'],
            'name': response_data['name']
        }


class FacebookView(BaseAuthView):

    provider = 'facebook'

    def get_backend_user(self, validated_data):
        access_token_url = 'https://graph.facebook.com/oauth/access_token'
        graph_api_url = 'https://graph.facebook.com/me'

        params = {
            'client_id': validated_data['client_id'],
            'redirect_uri': validated_data['redirect_uri'],
            'client_secret': FACEBOOK_SECRET,
            'code': validated_data['code']
        }

        # Step 1. Exchange authorization code for access token.
        r = requests.get(access_token_url, params=params)
        self.check_response(r)
        access_token = dict(parse_qsl(r.text))

        # Step 2. Retrieve information about the current user.
        r = requests.get(graph_api_url, params=access_token)
        self.check_response(r)
        response_data = r.json()

        return {
            'id': response_data['id'],
            'name': response_data['name']
        }

    def check_response(self, r, valid_response=requests.codes.ok):
        if r.status_code != valid_response:
            try:
                data = r.json()
                error_message = data['error']
            except:
                values = (r.reason, r.status_code)
                error_message = 'Message: %s, status code: %s' % values
            raise FacebookException(error_message)


class RegistrationView(generics.CreateAPIView):
    permission_classes = ()
    authentication_classes = ()
    serializer_class = RegistrationSerializer

    def perform_create(self, serializer):
        user = serializer.save()
        user.is_active = False
        user.save()
        tasks.send_activation_email.delay(user.uuid.hex)


class ActivationView(views.APIView):
    permission_classes = ()
    authentication_classes = ()

    def post(self, request):
        serializer = ActivationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        serializer.user.is_active = True
        serializer.user.save()

        token = Token.objects.get(user=serializer.user)
        return response.Response({'token': token.key}, status=status.HTTP_201_CREATED)
