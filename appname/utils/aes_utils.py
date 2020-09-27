import base64

from Crypto.Cipher import AES

from appname.config import BaseConfig


# AES_KEY = '0000000000000000'


def add_to_16(s):
    s = s.encode('utf-8')
    while len(s) % 16 != 0:
        s += b'\x00'
    return s


def aes_encrypt(raw_str):
    raw_str = add_to_16(raw_str)
    aes = AES.new(BaseConfig.AES_KEY, AES.MODE_ECB)
    encrypt_aes = aes.encrypt(raw_str)
    encrypted_text = base64.encodebytes(encrypt_aes).decode('utf-8').strip()
    return encrypted_text


def aes_decrypt(encrypt_str):
    aes = AES.new(BaseConfig.AES_KEY, AES.MODE_ECB)
    base64_decrypted = base64.decodebytes(encrypt_str.encode('utf-8'))
    decrypted_text_byte = aes.decrypt(base64_decrypted)
    decrypted_text_byte = decrypted_text_byte
    decrypted_text = decrypted_text_byte.decode('utf-8').strip('\0')
    return decrypted_text


if __name__ == "__main__":
    raw_str = 'ab123456'
    print(raw_str)
    print(raw_str.encode())
    encrypt_str = aes_encrypt(raw_str)
    print(encrypt_str)
    # res = aes_decrypt('aHQ50igoOyQCaMtf5bj1gXfU81ZTeyD2qm+DZEJI+kg=')
    res = aes_decrypt(encrypt_str)
    print(res)
    print(res.encode())


