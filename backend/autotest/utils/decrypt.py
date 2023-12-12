"""
# -*- coding:utf-8 -*-
# @Author: Beck
# @File: decrypt.py
# @Date: 2023/12/12 12:55
"""
import base64

from Cryptodome.Cipher import PKCS1_v1_5
from Cryptodome.PublicKey import RSA
from Cryptodome import Random

PUBLIC_KEY = """-----BEGIN PUBLIC KEY-----
MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQCJe2LpAURKi1nEWVZy91kIEz61
iDakpYTRnGedKfCBkk8q+lj6D5+tMpUDJrhUD0vBe24p6QAmF2WLTsliePyV2Nli
fsRdtwtpInC/HGJzuFE6lUXmJ7U3vZCRzOABb/Ab/da57b+ZdFdgbJlPQvG9FbY3
StHWKciJO/KmLiGrWQIDAQAB
-----END PUBLIC KEY-----"""

PRIVATE_KEY = """-----BEGIN RSA PRIVATE KEY-----
MIICXQIBAAKBgQCJe2LpAURKi1nEWVZy91kIEz61iDakpYTRnGedKfCBkk8q+lj6
D5+tMpUDJrhUD0vBe24p6QAmF2WLTsliePyV2NlifsRdtwtpInC/HGJzuFE6lUXm
J7U3vZCRzOABb/Ab/da57b+ZdFdgbJlPQvG9FbY3StHWKciJO/KmLiGrWQIDAQAB
AoGAQ3yMfJlRFxCZk49RJuUxUIv14/GF9UOE08oleJouQ8R41T2H8NQ7iy8Bw8a9
hBHwG32GAc+s8YXZpE0cARknz4STmaxy0SMQxyYDgbH+dKmGqLMLRTIyUAoYktG0
K/fG0jWkP9IxJz4WABX/siwpAr1HQbt1AY1RIxkt+r8kqtsCQQC1JFFKBawOQ4iT
F5kfbPliqCalPl+edq1/wM0jLnPldugCBYajwa3uocGUyQCkl3Rwc7REUZXa9GsW
3IujqObjAkEAwkwf1fAoYjeo7hYSdc1EUY1Bndn7dh05P+1rPbiO5el1Am4nAsug
5N5VjK8J+z6ITdZvgfcaFL2WI5Tsrys9kwJBAKoaQ7fWYb83Tf6LT4DCTeKGc1wD
mbluSvlILZtXGQCny7FyTQBkdZg9EFNO+iqWC4M6NFNfpfDqS9I5I2x5xO8CQGgB
7ADP4C5DcVCRzCv3R50IKpnfODbQCfdolkGh7Ayy3goBAS0D6Arb4Zu/j25I2Roh
ses2ZWW43wgJDnHuibUCQQCs05soaJpAe34Xoz2eTSaQ4MjB4Kp4ZdS7+Uwz8Co1
r1y8092OHw0SM4p6rrm3YOj+VXmCOdWsQ5oKZ35WPrFE
-----END RSA PRIVATE KEY-----"""


def generate_secret_key():
    """
    生成秘钥
    :return:
    """
    random_generator = Random.new().read  # 随机生成
    rsa = RSA.generate(1024, random_generator) # 秘钥位数和随机生成数
    private_key = rsa.export_key()
    public_key = rsa.publickey().export_key()
    print(private_key.decode('utf8'))
    print(public_key.decode('utf8'))
    return private_key.decode('utf8'), public_key.decode('utf8')


def encrypt_rsa_password(password):
    """
    密码加密
    :param password:
    :return:
    """
    try:
        public_key = RSA.import_key(PUBLIC_KEY)     # 导入公钥
        cipher = PKCS1_v1_5.new(public_key)     # 创建一个新的 PKCS1_v1_5 密码器
        text = base64.b64encode(cipher.encrypt(password.encode())) #密码器和公钥对密码进行加密。使用 base64 编码将加密后的密码转换为字符串
        return text.decode()
    except Exception as e:
        return password, e


def decrypt_rsa_password(password):
    """
    密码解密
    :param password:
    :return:
    """
    try:
        private_key = RSA.import_key(PRIVATE_KEY) # 导入私钥
        cipher = PKCS1_v1_5.new(private_key)    # 创建一个新的 PKCS1_v1_5 密码器
        text = cipher.decrypt(base64.b64decode(password), b'') # 密码器和私钥对密码进行解密
        return text.decode()

    except Exception as e:
        return password, e


if __name__ == '__main__':
    print(encrypt_rsa_password('123456'))
    print(decrypt_rsa_password(
        'BvdwJMMwxWbgWY8TSXP50oD2YcZwqZhAv/w1gL/y6z6kKkib+0ys0rebw3z6KkFBFBabNQubnr+XFvKuN6w5xvhS/4iDj4OMBSjDNlH2Ie1ky2L3Ax8C8eB0Pv4fJSPyIFS2B9ilqltp7jTEInwWgnNlqOXrZFdiGuM0j2pXVW0='))
