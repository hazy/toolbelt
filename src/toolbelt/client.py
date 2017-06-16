"""Web service API client."""

import base64
import click
import hashlib
import hmac
import requests

from . import aes
from . import util

class Client(object):
    """HMAC authenticated API client."""

    def __init__(self, endpoint, key, secret):
        self.endpoint = endpoint
        self.key = key
        self.secret = secret

    def auth_headers(self):
        key = self.key.encode('utf-8')
        secret = self.secret.encode('utf-8')
        signed_data = util.unique_hash().encode('utf-8')
        h = hmac.new(secret, signed_data, hashlib.sha256)
        signature = h.hexdigest().encode('utf-8')
        enc_signature = base64.b64encode(signature).decode('utf-8')
        enc_signed_data = base64.b64encode(signed_data).decode('utf-8')
        enc_key = base64.b64encode(key).decode('utf-8')
        return {
            'Authorization': 'HMAC: {0}'.format(enc_signature),
            'X-Client-Key': enc_key,
            'X-Signed-Data': enc_signed_data,
        }

    def wrap(self, response):
        code = response.status_code
        if code == 403:
            msg = 'Forbidden. Have you logged in with the right credentials?'
            click.secho(msg, fg='red')
            raise click.Abort()
        if code != 200:
            msg = 'Error {0}. Please try again.'.format(response)
            click.secho(msg, fg='red')
            raise click.Abort()
        return response

    def post(self, path, data):
        url = self.endpoint + path
        headers = self.auth_headers()
        r = requests.post(url, headers=headers, json=data)
        return self.wrap(r)

    def upload(self, path, file_, key):
        url = self.endpoint + path
        iv = util.random_bytes(16)
        headers = self.auth_headers()
        headers['X-IV'] = base64.b64encode(iv)
        iter_chunks = aes.gen_encrypted_chunks(file_, key, iv)
        r = requests.post(url, data=iter_chunks, headers=headers)
        return self.wrap(r)
