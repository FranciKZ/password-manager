import base64
import hashlib
import secrets
import string
from Crypto import Random
from Crypto.Cipher import AES

BS = 16
pad = lambda s: s + (BS - len(s) % BS) * chr(BS - len(s) % BS).encode()
unpad = lambda s: s[:-ord(s[len(s)-1:])]

def iv():
    return chr(0) * 16

class PasswordEncryption(object):    
    def __init__(self, key):
        self.key = key

    def genPassword():
        alphabet = string.ascii_letters + string.digits
        password = ''.join(secrets.choice(alphabet) for i in range(20))
        return password

    def encryptPassword(self, password):
        password = password.encode()
        raw = pad(password)
        cipher = AES.new(self.key, AES.MODE_CBC, iv())
        enc = cipher.encrypt(raw)
        return base64.b64encode(enc).decode('utf-8')

    def decryptPassword(self, enc):
        enc = base64.b64ecord(enc)
        cipher = AES.new(self.key, AES.MODE_CBC, iv())
        dec = cipher.decrypt(enc)
        return unpad(dec).decode('utf-8')
"""
class DatabaseEncryption:
    def encryptDB():
        return encryptedDB

    def unencryptDB():
        return unencryptedDB
"""

key = 'abcdefghijklmnopqrstuvwxyz123456'
password = 'FrancisRules'
_enc = 'gOXlygE+qxS+69zN5qC6eKJvMiEoDQtdoJb3zjT8f/E='

enc = PasswordEncryption(key).encryptPassword(message)
dec = PasswordEncryption(key).decryptPassword(_enc)

print(_enc == enc)
print(message == dec)