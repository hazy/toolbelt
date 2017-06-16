from Crypto.Cipher import AES
from Crypto.Util import Counter

def gen_encrypted_chunks(file_, key, iv):
    iv_long = int.from_bytes(iv, byteorder='big')
    counter = Counter.new(128, initial_value=iv_long)
    cipher = AES.new(key, AES.MODE_CTR, counter=counter)
    while True:
        chunk = file_.read(4096)
        if not chunk:
            break
        yield cipher.encrypt(chunk)
