"""Web service API client."""

import base64
import hashlib
import hmac
import requests

from . import util

class Client(object):
    """HMAC authenticated API client."""

    def __init__(self, endpoint, key, secret):
        self.endpoint = endpoint
        self.key = key
        self.secret = secret

    def auth_headers(self):
        signed_data = util.unique_hash()
        h = hmac.new(self.secret.encode('utf-8'), signed_data, hashlib.sha256)
        enc_signature = base64.b64encode(h.hexdigest())
        enc_signed_data = base64.b64encode(signed_data)
        enc_key = base64.b64encode(self.key)
        return {
            'Authorization': 'HMAC: {0}'.format(enc_signature),
            'X-Client-Key': enc_key,
            'X-Signed-Data': enc_signed_data,
        }

    def post(self, path, data):
        url = self.endpoint + path
        headers = self.auth_headers()
        return requests.post(url, headers=headers, json=data)
