# coding: utf-8

import re
import struct
import xml.sax
import base64
import requests
from dict2xml import dict2xml
from xml2dict import xml2dict
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5
from Crypto.Hash import SHA, MD5


# 通联公钥证书
CERT_KEY = """-----BEGIN CERTIFICATE-----
MIIDUzCCAjugAwIBAgIISfeJoESLF2YwDQYJKoZIhvcNAQEFBQAwNzEVMBMGA1UE
AwwMQWxsaW5wYXlUZXN0MREwDwYDVQQKDAhBbGxpbnBheTELMAkGA1UEBhMCQ04w
HhcNMTIwNzI0MDgzNDQxWhcNMTQwNzI0MDgzNDQxWjAbMRkwFwYDVQQDDBBhbGxp
bnBheS1wZHN0ZXN0MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAr/Q9
RgEiYtJjmWV2Y3goQ1JpTAddkGE8Vb+ibdvv64n4i5UoWjHP/f2e7O2XYg9K2ZEN
XH/3UlXYJGO7mqElCdnqQSKKJ3SBpCQGKFF5tDuUqj8FiurUgXhIIr4JFuYZF6FE
2aXv5oYLxkbVmRgoXgpHPYIokr26Uvu4HQuFqNlfglghpDUPjGT5AnLqiwsMQaAf
X5GCpHGUhYeSE6z78lDdE3fTGFQPf+73FSfSReXgfGPRLALXxmODBOU67QYX6YYf
kHATt3LQVhjg5WklIa+yO5qSzGDXYWq8SCkTInxK+xyF5UZESRTPfO6P1QTK/6Kv
AFSUp/H45SF1HaiJ7QIDAQABo38wfTAdBgNVHQ4EFgQUH7cyXSYGu2tJg3+UT+TP
WfiMU64wDAYDVR0TAQH/BAIwADAfBgNVHSMEGDAWgBSJi2vLySxYZPaAM5Nuw+5f
N+Qe8jAOBgNVHQ8BAf8EBAMCBeAwHQYDVR0lBBYwFAYIKwYBBQUHAwIGCCsGAQUF
BwMEMA0GCSqGSIb3DQEBBQUAA4IBAQAwpbsN8LH/y1NITh3j6FrC8SCrPDlU67hA
lMY3p0yamS7kxwlnogyO8r9eGx7leDvFJymfJoKuha1SU438ipXx/kMmSUnSLyIF
aEnOnr8ZZ6P5EFrD9Mmk4vqmusZZ2koACl1OOSb+SES3R7j6WM8gObPaoiY9xxYh
d1HHulFGARsPvfSF4sfwVJlonBRDoG9xjnmYeZFH7RYR3N5e5kg20XCAuE39fgcx
W0TvvOQCYIwYrV3E8isIm1s9gDVHO+pt8MOFSBnPGhuyymkwKo/8JTEER1Gmx5/e
mZfc0V8zYIWy3Vk2RObQkiCUX2f6ja+qggZTha/QtDdVGQggxro/
-----END CERTIFICATE-----"""

#
# CERT_KEY = """-----BEGIN PUBLIC KEY-----
# MIIDUzCCAjugAwIBAgIISfeJoESLF2YwDQYJKoZIhvcNAQEFBQAwNzEVMBMGA1UE
# AwwMQWxsaW5wYXlUZXN0MREwDwYDVQQKDAhBbGxpbnBheTELMAkGA1UEBhMCQ04w
# HhcNMTIwNzI0MDgzNDQxWhcNMTQwNzI0MDgzNDQxWjAbMRkwFwYDVQQDDBBhbGxp
# bnBheS1wZHN0ZXN0MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAr/Q9
# RgEiYtJjmWV2Y3goQ1JpTAddkGE8Vb+ibdvv64n4i5UoWjHP/f2e7O2XYg9K2ZEN
# XH/3UlXYJGO7mqElCdnqQSKKJ3SBpCQGKFF5tDuUqj8FiurUgXhIIr4JFuYZF6FE
# 2aXv5oYLxkbVmRgoXgpHPYIokr26Uvu4HQuFqNlfglghpDUPjGT5AnLqiwsMQaAf
# X5GCpHGUhYeSE6z78lDdE3fTGFQPf+73FSfSReXgfGPRLALXxmODBOU67QYX6YYf
# kHATt3LQVhjg5WklIa+yO5qSzGDXYWq8SCkTInxK+xyF5UZESRTPfO6P1QTK/6Kv
# AFSUp/H45SF1HaiJ7QIDAQABo38wfTAdBgNVHQ4EFgQUH7cyXSYGu2tJg3+UT+TP
# WfiMU64wDAYDVR0TAQH/BAIwADAfBgNVHSMEGDAWgBSJi2vLySxYZPaAM5Nuw+5f
# N+Qe8jAOBgNVHQ8BAf8EBAMCBeAwHQYDVR0lBBYwFAYIKwYBBQUHAwIGCCsGAQUF
# BwMEMA0GCSqGSIb3DQEBBQUAA4IBAQAwpbsN8LH/y1NITh3j6FrC8SCrPDlU67hA
# lMY3p0yamS7kxwlnogyO8r9eGx7leDvFJymfJoKuha1SU438ipXx/kMmSUnSLyIF
# aEnOnr8ZZ6P5EFrD9Mmk4vqmusZZ2koACl1OOSb+SES3R7j6WM8gObPaoiY9xxYh
# d1HHulFGARsPvfSF4sfwVJlonBRDoG9xjnmYeZFH7RYR3N5e5kg20XCAuE39fgcx
# W0TvvOQCYIwYrV3E8isIm1s9gDVHO+pt8MOFSBnPGhuyymkwKo/8JTEER1Gmx5/e
# mZfc0V8zYIWy3Vk2RObQkiCUX2f6ja+qggZTha/QtDdVGQggxro/
# -----END PUBLIC KEY-----"""
CERT_KEY = """-----BEGIN PUBLIC KEY-----
MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQDR4Wq9l44lw/thTPyFmSi2hII9
2EPh90yGXQNL5e7zJPD16j6Qtr+tIPNSQaVrnmNwrtqyEC2x4Meyp3tdCWPYUF11
r2GgDgxKfUByetNG4XqJeUKkkJ6D6C706mTf/2zsm8KFoNYCYPX1GhvpiTOikHcN
lHLCnOD7jbMAovJg/QIDAQAB
-----END PUBLIC KEY-----"""
# 商户私钥证书
PRIVATE_KEY = """-----BEGIN PRIVATE KEY-----
MIICdgIBADANBgkqhkiG9w0BAQEFAASCAmAwggJcAgEAAoGBAKUnz6CP8TzBs/nT
YQHWYbe86Qcos6hzRvNa4c/0ICSVD3O+5HV4m1SXu6K5IxSRfAsmWAO0YpUZTri+
lx0UAdtvQEW1ljQxRye5Fidg0+PLkViAK+ICG5xq2BRYTnughbR9SW7htFIn6Dn4
6VzdRjWScZoKqkkB9EFVxJd6JmO/AgMBAAECgYEAhEye611Df0sgNEmbFRC6GKjQ
9zYorREjTgCIkcBbG1L5HNxXQK8LpzkhSxoJuwlMF9ZwfQ88RXoPcLjkbpu/W8sI
zJflJcMSzLiQLHQkPCP0FkS41ulRy7rRXuXc/FaqOsaA7TSLT6STZYiZzuRf68cD
Jk4rvjeTK5QS8RMJL8ECQQD+mRe1WV1/v1gqAc/LJquTUYM/GT6PIMfLRB6ckfQv
53K4x6+gPYpSkcCd0Ti8VRrJ8mZ7/JjQt9vXgRcrXGFhAkEAphChkgFyetrZmi7q
9ESvcuUyS2t09ncgdNE91Trvm9k6gNSROybMg9/ZIYSzDTkY6nhlvhNhmYcp7GCb
ZUg5HwJAYY4X341WnlSbW71F+fnfVJuvRsZNilptNB3t/OCQSKrO8q7RRP1Pu0PO
IqrAqqmRkkAntOqdQ5yvyGvWjO7hAQJAaDwoLi0aXmLgExdAAvLZ7ZRPbWeVkt5T
UP/FgAHuRDSltBe40RgZZu0qrQ9OFA6yxPmtYxFnQabFeclpwLkEoQJAKN+9rqdi
OS1lUrLsefUjZ216i9leTgSGTSuz7zgudUNLpoqal7c38B0CLQ1qd39usnmXExa9
5l0krJ7Lrfq0Ww==
-----END PRIVATE KEY-----"""


# CERT_KEY = """MIIDUzCCAjugAwIBAgIISfeJoESLF2YwDQYJKoZIhvcNAQEFBQAwNzEVMBMGA1UEAwwMQWxsaW5wYXlUZXN0MREwDwYDVQQKDAhBbGxpbnBheTELMAkGA1UEBhMCQ04wHhcNMTIwNzI0MDgzNDQxWhcNMTQwNzI0MDgzNDQxWjAbMRkwFwYDVQQDDBBhbGxpbnBheS1wZHN0ZXN0MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAr/Q9RgEiYtJjmWV2Y3goQ1JpTAddkGE8Vb+ibdvv64n4i5UoWjHP/f2e7O2XYg9K2ZENXH/3UlXYJGO7mqElCdnqQSKKJ3SBpCQGKFF5tDuUqj8FiurUgXhIIr4JFuYZF6FE2aXv5oYLxkbVmRgoXgpHPYIokr26Uvu4HQuFqNlfglghpDUPjGT5AnLqiwsMQaAfX5GCpHGUhYeSE6z78lDdE3fTGFQPf+73FSfSReXgfGPRLALXxmODBOU67QYX6YYfkHATt3LQVhjg5WklIa+yO5qSzGDXYWq8SCkTInxK+xyF5UZESRTPfO6P1QTK/6KvAFSUp/H45SF1HaiJ7QIDAQABo38wfTAdBgNVHQ4EFgQUH7cyXSYGu2tJg3+UT+TPWfiMU64wDAYDVR0TAQH/BAIwADAfBgNVHSMEGDAWgBSJi2vLySxYZPaAM5Nuw+5fN+Qe8jAOBgNVHQ8BAf8EBAMCBeAwHQYDVR0lBBYwFAYIKwYBBQUHAwIGCCsGAQUFBwMEMA0GCSqGSIb3DQEBBQUAA4IBAQAwpbsN8LH/y1NITh3j6FrC8SCrPDlU67hAlMY3p0yamS7kxwlnogyO8r9eGx7leDvFJymfJoKuha1SU438ipXx/kMmSUnSLyIFaEnOnr8ZZ6P5EFrD9Mmk4vqmusZZ2koACl1OOSb+SES3R7j6WM8gObPaoiY9xxYhd1HHulFGARsPvfSF4sfwVJlonBRDoG9xjnmYeZFH7RYR3N5e5kg20XCAuE39fgcxW0TvvOQCYIwYrV3E8isIm1s9gDVHO+pt8MOFSBnPGhuyymkwKo/8JTEER1Gmx5/emZfc0V8zYIWy3Vk2RObQkiCUX2f6ja+qggZTha/QtDdVGQggxro/"""
PRIVATE_KEY = """MIICdgIBADANBgkqhkiG9w0BAQEFAASCAmAwggJcAgEAAoGBAKUnz6CP8TzBs/nTYQHWYbe86Qcos6hzRvNa4c/0ICSVD3O+5HV4m1SXu6K5IxSRfAsmWAO0YpUZTri+lx0UAdtvQEW1ljQxRye5Fidg0+PLkViAK+ICG5xq2BRYTnughbR9SW7htFIn6Dn46VzdRjWScZoKqkkB9EFVxJd6JmO/AgMBAAECgYEAhEye611Df0sgNEmbFRC6GKjQ9zYorREjTgCIkcBbG1L5HNxXQK8LpzkhSxoJuwlMF9ZwfQ88RXoPcLjkbpu/W8sIzJflJcMSzLiQLHQkPCP0FkS41ulRy7rRXuXc/FaqOsaA7TSLT6STZYiZzuRf68cDJk4rvjeTK5QS8RMJL8ECQQD+mRe1WV1/v1gqAc/LJquTUYM/GT6PIMfLRB6ckfQv53K4x6+gPYpSkcCd0Ti8VRrJ8mZ7/JjQt9vXgRcrXGFhAkEAphChkgFyetrZmi7q9ESvcuUyS2t09ncgdNE91Trvm9k6gNSROybMg9/ZIYSzDTkY6nhlvhNhmYcp7GCbZUg5HwJAYY4X341WnlSbW71F+fnfVJuvRsZNilptNB3t/OCQSKrO8q7RRP1Pu0POIqrAqqmRkkAntOqdQ5yvyGvWjO7hAQJAaDwoLi0aXmLgExdAAvLZ7ZRPbWeVkt5TUP/FgAHuRDSltBe40RgZZu0qrQ9OFA6yxPmtYxFnQabFeclpwLkEoQJAKN+9rqdiOS1lUrLsefUjZ216i9leTgSGTSuz7zgudUNLpoqal7c38B0CLQ1qd39usnmXExa95l0krJ7Lrfq0Ww=="""
# 商户私钥密码以及用户密码
password = '111111'
# 通联系统对接请求地址（外网,商户测试时使用）
apiUrl = 'http://113.108.182.3:8083/aipg/ProcessServlet'


def hex2bin(hexstr):
    n = len(hexstr)
    sbin = ''
    i = 0
    while i < n:
        a = hexstr[i:i+2]
        print a
        c = struct.pack('H*', a)
        if i == 0:
            sbin = c
        else:
            sbin += c
        i += 2
    return sbin


def verifyXml(xmlResponse):
    """验签
    """
    print xmlResponse
    dictResponse = xml2dict(xmlResponse, custom_root='AIPG')

    signature = dictResponse['INFO'].pop('SIGNED_MSG')

    xmlResponseSrc = dict2xml(dictResponse, custom_root='AIPG', encoding='GBK')
    print '验签原文', xmlResponseSrc.decode('GBK')

    flag = verifyStr(xmlResponseSrc, signature, CERT_KEY)
    if (flag):
        # 变成数组，做自己相关业务逻辑
        return dictResponse
    else:
        return False


def signXml(params):
    """签名
    """
    xmlSignSrc = dict2xml(params, custom_root='AIPG', encoding='GBK')
    xmlSignSrc = xmlSignSrc.replace('TRANS_DETAIL2', 'TRANS_DETAIL')

    params['INFO']['SIGNED_MSG'] = signStr(xmlSignSrc, PRIVATE_KEY, password)

    xmlSignPost = dict2xml(params, custom_root='AIPG', encoding='GBK')

    return  xmlSignPost


def send(params):
    """发送请求
    """
    xmlSignPost = signXml(params)
    print xmlSignPost
    xmlSignPost = xmlSignPost.replace('TRANS_DETAIL2', 'TRANS_DETAIL')
    #response = requests.post(apiUrl, xmlSignPost)
    #print response
    #xmlResponse = response.text
    xmlResponse = u'<?xml version="1.0" encoding="GBK"?><AIPG>\n  <INFO>\n    <TRX_CODE>200004</TRX_CODE>\n    <VERSION>03</VERSION>\n    <DATA_TYPE>2</DATA_TYPE>\n    <REQ_SN>200604000000445-rrrr1356732135xxxx</REQ_SN>\n    <RET_CODE>1000</RET_CODE>\n    <ERR_MSG>\u7528\u6237\u6216\u5bc6\u7801\u9519\u8bef</ERR_MSG>\n    <SIGNED_MSG>238d472508cd240925277e3d34fda9febd01333bc20f824faddffcc3979ae465e6aa1c07e8c888bfd3cab102b7855b7f078526f3c3331a71c30d1f8966b53d82c48a77f260a35f85653123640005a6eaa696871a325c66dd4968a9b4447f2bb4bc98d34ce17bfad7cff9bb79bb795f2e2bb2f86e7b05449d71d322848ce2e3d7df4ff2effd582e714523e4c65b37f34b500e5cb4b8a05e8dac7669ba3fe8443757e958f225227c497d6afec087dc37a13fbc5b36d8021ce5aae16b13e87c70519caec3cea93a797efffbcf7f009482d4d28d5802f50ba4f3880b56efb2ce571ffd021aec4d1f0afd497dc667e64158b960d79fec1101a64791bded1896578ffd</SIGNED_MSG>\n  </INFO>\n</AIPG>'
    print repr(xmlResponse)
    print xmlResponse
    print xml2dict(xmlResponse, custom_root='AIPG')
    result = verifyXml(xmlResponse)
    return result


def signStr(data, pri_key, passphrase=None):
    """RSA签名
    Args:
        data: 待签名数据
        pri_key: 私钥
        passphrase: 私钥密码
    Returns:
        Sign签名，需要用base64编码
    """
    key_der = base64.b64decode(pri_key)
    rsakey = RSA.importKey(key_der, passphrase)
    signer = PKCS1_v1_5.new(rsakey)
    h = MD5.new(data)
    signature = base64.b16encode(signer.sign(h)).lower()
    print '签名成功： ', signature
    return signature


def verifyStr(data, signature, pub_key):
    """RSA验签
    Args:
        data: 待签名数据
        signature: signature需要验签的签名
        pub_key: 验签用公钥
    Returns:
        验签是否通过 bool值
    """
    #key_der = base64.b64decode(pub_key)
    key_der = pub_key
    print repr(key_der)
    key = RSA.importKey(key_der)
    h = SHA.new(data)
    verifier = PKCS1_v1_5.new(key)
    if verifier.verify(h, signature):
        print '验签成功'
        return True
    else:
        print '验签失败'
        return False


if __name__ == '__main__':
    xmlstr = u"""<?xml version="1.0" encoding="GBK"?><AIPG>
  <INFO>
    <TRX_CODE>100011</TRX_CODE>
    <VERSION>03</VERSION>
    <DATA_TYPE>2</DATA_TYPE>
    <LEVEL>5</LEVEL>
    <MERCHANT_ID>200581000000519</MERCHANT_ID>
    <USER_NAME>20058100000051902</USER_NAME>
    <USER_PASS>111111</USER_PASS>
    <REQ_SN>1377051780610</REQ_SN>
    <SIGNED_MSG>4b560e777597045d7273e73865671f3af7a34db15a3000eb7f5247090137f8e1feec91977364b6716f7407a7e540a8664048029832c18fdfcb37086bd2462310644a8ba3f81ce2001959219e7564dbb83a15aeae579ac814853be5e6bac7047dd108dcd37790b4ea0956118924c3a08e9e72e0baacfc74ba0298ac627769c07f</SIGNED_MSG>
  </INFO>
  <TRANS>
    <BUSINESS_CODE>10600</BUSINESS_CODE>
    <MERCHANT_ID>200581000000519</MERCHANT_ID>
    <SUBMIT_TIME>20130821102300</SUBMIT_TIME>
    <BANK_CODE>0105</BANK_CODE>
    <ACCOUNT_NO>622588121251757643</ACCOUNT_NO>
    <ACCOUNT_NAME>测试试</ACCOUNT_NAME>
    <ACCOUNT_PROP>0</ACCOUNT_PROP>
    <AMOUNT>100000</AMOUNT>
    <CURRENCY>CNY</CURRENCY>
    <TEL>13434245846</TEL>
    <CUST_USERID>252523524253xx</CUST_USERID>
  </TRANS>
</AIPG>"""
    dictstr = xml2dict(xmlstr, custom_root='AIPG')
    sign = dictstr['INFO'].pop('SIGNED_MSG')
    xmlsrc = dict2xml(dictstr, custom_root='AIPG', encoding='GBK')
    print xmlsrc
    print signStr(xmlsrc, PRIVATE_KEY, password)
    print sign
