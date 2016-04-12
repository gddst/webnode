import base64
import binascii
import hashlib
import os
import pprint


class SecurityUtil(object):
    
    @staticmethod
    def Hash_pw(password):
        return hashlib.sha256(password).hexdigest()
    
    @staticmethod
    def salted_hash_pw(password):
        salt=binascii.hexlify(os.urandom(32))
        salted_pw=hashlib.sha256(salt+password).hexdigest()
        return salt+':'+salted_pw
    
    @staticmethod
    def validate_pw(salted_has_pw, password):
        salt=salted_has_pw.split(':')[0]
        pw=salted_has_pw.split(':')[1]
        return hashlib.sha256(salt+password).hexdigest()==pw
        
if __name__=="__main__":
    pass