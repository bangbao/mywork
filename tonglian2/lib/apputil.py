# coding: utf-8

import hashlib
import urllib


def force_str(string):
    if isinstance(string, unicode):
        return string.encode('utf-8')
    return str(string)


def sign_array(array, appkey):
    """签名
    """
    array['key'] = appkey
    sign_value = ToUrlParams(sorted(array.iteritems()))
    print sign_value
    return hashlib.md5(sign_value).hexdigest()


def valid_sign(array, appkey):
    """校验签名
    """
    sign = array.pop('sign', '')
    my_sign = sign_array(array, appkey)
    return sign == my_sign


def ToUrlParams(array):
    if hasattr(array, 'items'):
        array = array.items()
    params_lsit = []
    for k, v in array:
        if not v:
            continue
        params_lsit.append('%s=%s' % (force_str(k), force_str(v)))
    return '&'.join(params_lsit)


if __name__ == '__main__':
    params = {
        'appid': '00000000',
        'cusid': '990440153996000',
        'paytype': '0',
        'trxamt': '1',
        'reqsn': '1450432107647',
        'randomstr': '1450432107647',
        'body': u'商品名称',
        'remark': '备注信息',
    }
    key = '43df939f1e7f5c6909b3f4b63f893994'
    sign = '1918CC7DBBD120B1BB130C9400186F79'.lower()
    my_sign = sign_array(params, key)
    print '%s %s==%s' % (sign==my_sign, sign, my_sign)