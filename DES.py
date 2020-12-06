# -*- coding: utf-8 -*-
import uuid
import base64
from pyDes import des, CBC, PAD_PKCS5

secret_key = 'ST83=@XV'

iv = [1, 2, 3, 4, 5, 6, 7, 8]


def encode(s):
    k = des(secret_key, CBC, iv, pad=None, padmode=PAD_PKCS5)
    s_encrypt = k.encrypt(s, padmode=PAD_PKCS5)
    return bytes.decode(base64.b64encode(s_encrypt))


def decode(s):
    k = des(secret_key, CBC, iv, pad=None, padmode=PAD_PKCS5)
    s_decrypt = k.decrypt(base64.b64decode(s), padmode=PAD_PKCS5)
    return bytes.decode(s_decrypt)

def GetExtension(userID):
    Extension = '{"systemName":"android",' \
                '"systemVersion":"n.m.s",' \
                '"model":"fucker",' \
                '"deviceId":"' + str(uuid.uuid1()) + '",' \
                '"appVersion":"8.2.10",' \
                '"lon":' + '110.33493' + ',' \
                '"lat":' + '20.063253' + ',' \
                '"userId":"' + userID + '"}'
    return encode(Extension)