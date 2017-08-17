# coding: utf-8

import re
import struct
import xml.sax
import base64
import binascii
import requests
from dict2xml import dict2xml
from xml2dict import xml2dict
from Crypto.Hash import SHA
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5
from Crypto.Util.asn1 import DerSequence


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

# 商户私钥密码以及用户密码
password = '111111'
# 通联系统对接请求地址（外网,商户测试时使用）
apiUrl = 'http://113.108.182.3:8083/aipg/ProcessServlet'


def verifyXml(xmlResponse):
    """验签
    """
    xmlResponse = xmlResponse.encode('GBK')
    signature = re.findall('<SIGNED_MSG>(.*)</SIGNED_MSG>', xmlResponse)[0]
    xmlResponseSrc = re.sub('<SIGNED_MSG>.*</SIGNED_MSG>', '', xmlResponse)

    print '验签原文', xmlResponseSrc.decode('GBK')

    flag = verifyStr(xmlResponseSrc, signature, CERT_KEY)
    if (flag):
        # 变成数组，做自己相关业务逻辑
        return xml2dict(xmlResponse, custom_root='AIPG', encoding='GBK')
    else:
        return False


def verifyStr(data, signature, pub_key):
    """RSA验签
    Args:
        data: 待签名数据
        signature: signature需要验签的签名
        pub_key: 验签用公钥
    Returns:
        验签是否通过 bool值
    """
    lines = pub_key.replace(" ", '').split()
    der = binascii.a2b_base64(''.join(lines[1:-1]))
    cert = DerSequence()
    cert.decode(der)
    tbsCertificate = DerSequence()
    tbsCertificate.decode(cert[0])
    subjectPublicKeyInfo = tbsCertificate[6]
    rsa_key = RSA.importKey(subjectPublicKeyInfo)
    h = SHA.new(data)
    verifier = PKCS1_v1_5.new(rsa_key)
    signature = binascii.a2b_hex(signature)
    if verifier.verify(h, signature):
        print u'验签成功'
        return True
    else:
        print u'验签失败'
        return False


def signXml(params):
    """签名
    """
    xmlSignSrc = dict2xml(params, custom_root='AIPG', encoding='GBK')
    xmlSignSrc = xmlSignSrc.replace('TRANS_DETAIL2', 'TRANS_DETAIL')

    params['INFO']['SIGNED_MSG'] = signStr(xmlSignSrc, PRIVATE_KEY, password)

    xmlSignPost = dict2xml(params, custom_root='AIPG', encoding='GBK')

    return  xmlSignPost


def signStr(data, pri_key, passphrase=None):
    """RSA签名
    Args:
        data: 待签名数据
        pri_key: 私钥
        passphrase: 私钥密码
    Returns:
        Sign签名，需要用base64编码
    """
    rsakey = RSA.importKey(pri_key, passphrase)
    signer = PKCS1_v1_5.new(rsakey)
    h = SHA.new(data)
    s = signer.sign(h)
    signature = binascii.b2a_hex(s)
    return signature


def send(params):
    """发送请求
    """
    xmlSignPost = signXml(params)
    xmlSignPost = xmlSignPost.replace('TRANS_DETAIL2', 'TRANS_DETAIL')
    response = requests.post(apiUrl, xmlSignPost)
    xmlResponse = response.text
    #print repr(xmlResponse)
    result = verifyXml(xmlResponse)
    return result


if __name__ == '__main__':
    xmlstr = u"<?xml version=\"1.0\" encoding=\"GBK\"?><AIPG><INFO><TRX_CODE>200004</TRX_CODE><VERSION>03</VERSION><DATA_TYPE>2</DATA_TYPE><LEVEL>6</LEVEL><USER_NAME>20060400000044502</USER_NAME><USER_PASS>111111</USER_PASS><REQ_SN>200604000000445-rrrr1356732135xxxx</REQ_SN></INFO><QTRANSREQ><QUERY_SN>22222222222222222222222</QUERY_SN><MERCHANT_ID>200604000000445</MERCHANT_ID><STATUS>2</STATUS><TYPE>1</TYPE><START_DAY/><END_DAY/></QTRANSREQ></AIPG>"
    mersign = '238d472508cd240925277e3d34fda9febd01333bc20f824faddffcc3979ae465e6aa1c07e8c888bfd3cab102b7855b7f078526f3c3331a71c30d1f8966b53d82c48a77f260a35f85653123640005a6eaa696871a325c66dd4968a9b4447f2bb4bc98d34ce17bfad7cff9bb79bb795f2e2bb2f86e7b05449d71d322848ce2e3d7df4ff2effd582e714523e4c65b37f34b500e5cb4b8a05e8dac7669ba3fe8443757e958f225227c497d6afec087dc37a13fbc5b36d8021ce5aae16b13e87c70519caec3cea93a797efffbcf7f009482d4d28d5802f50ba4f3880b56efb2ce571ffd021aec4d1f0afd497dc667e64158b960d79fec1101a64791bded1896578ffd'
    #mersign = re.findall('<SIGNED_MSG>(.*)</SIGNED_MSG>', xmlstr)[0]
    #xmlsrc = dict2xml(dictstr, custom_root='AIPG', encoding='GBK')
    xmlsrc = '64563425345325345|13434245847|245245|745635267|46346346346|345'
    #xmlsrc = re.sub('<SIGNED_MSG>.*</SIGNED_MSG>', '', xmlstr).encode('GBK')
    print xmlstr.encode('GBK')
    print
    print xmlsrc
    print signStr(xmlsrc, PRIVATE_KEY, password)
    #print mersign
