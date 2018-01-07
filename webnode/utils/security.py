import binascii
import hashlib
import os


class SecurityUtil(object):
    @staticmethod
    def Hash_pw(password):
        return hashlib.sha256(password).hexdigest()

    @staticmethod
    def salted_hash_pw(password):
        password = bytes(password, encoding='utf-8')
        salt = binascii.hexlify(os.urandom(32))
        salted_pw = hashlib.sha256(salt + password).hexdigest()
        salted_pw = bytes(salted_pw, encoding='utf-8')
        return salt + b':' + salted_pw

    @staticmethod
    def validate_pw(salted_has_pw, password):
        password = bytes(password, encoding='utf-8')
        salt = salted_has_pw.split(b':')[0]
        saved_hash = salted_has_pw.split(b':')[1]
        input_hash = bytes(hashlib.sha256(salt + password).hexdigest(), encoding='utf-8')
        return input_hash == saved_hash
