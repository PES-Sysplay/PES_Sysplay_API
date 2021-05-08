from django.conf import settings
from google.auth.transport import requests
from google.oauth2 import id_token


class GoogleOauth:
    def __init__(self, token):
        self.client_id = settings.GOOGLE_CLIENT_ID
        self.token = token

    def get_email(self):
        try:
            idinfo = id_token.verify_oauth2_token(self.token, requests.Request(), self.client_id)

            return idinfo['email']
        except ValueError:
            raise self.InvalidToken

    class InvalidToken(Exception):
        pass
