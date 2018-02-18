"""Web service API client."""

import base64
import click
from datetime import datetime
import hashlib
import hmac
import json
import requests
from urllib.parse import urlparse

from . import aes
from . import util

class Client(object):
    """HMAC authenticated API client."""

    def __init__(self, endpoint, key, secret):
        self.endpoint = endpoint
        self.key = key
        self.secret = secret

    def auth_headers(self, path, data):
        timestamp = datetime.utcnow().isoformat()
        parsed = urlparse(path)
        signed_data = '\n'.join([parsed.path,
                                 parsed.query,
                                 data,
                                 timestamp]).encode('utf-8')
        hashed_hex = hashlib.sha256(signed_data).hexdigest().encode('utf-8')
        key = self.key.encode('utf-8')
        secret = self.secret.encode('utf-8')
        h = hmac.new(secret, hashed_hex, hashlib.sha256)
        signature = h.hexdigest().encode('utf-8')
        enc_signature = base64.b64encode(signature).decode('utf-8')
        enc_key = base64.b64encode(key).decode('utf-8')
        return {
            'Authorization': 'HMAC: {0}'.format(enc_signature),
            'X-Client-Key': enc_key,
            'X-Anon-Timestamp' : timestamp,
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
        json_data = json.dumps(data)
        headers = self.auth_headers(path, json_data)
        headers['Content-Type'] = 'application/json'
        r = requests.post(url, headers=headers, data=json_data)
        return self.wrap(r)

    def upload(self, path, file_, key, encryption_key):
        url = self.endpoint + path
        iv = util.random_bytes(16)
        headers = self.auth_headers(path, '') # TODO: auth for uploads
        headers['X-IV'] = base64.b64encode(iv)
        if encryption_key:
            headers['X-ENCRYPTION-KEY'] = encryption_key
        iter_chunks = aes.gen_encrypted_chunks(file_, key, iv)
        r = requests.post(url, data=iter_chunks, headers=headers)
        return self.wrap(r)
