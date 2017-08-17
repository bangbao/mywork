# coding: utf-8

import time
from lib import tools


def single_time_verify():
    """单笔实时验证(三要素)
    验证卡号，户名，证件
    """
    params = {
        'INFO': tools.get_req_info('211003'),
        'VALIDR': {
            'MERCHANT_ID': tools.MERCHANT_ID,
            'SUBMIT_TIME': time.strftime('%Y%m%d%H%M%S'),
            'BANK_CODE': '0105',
            'ACCOUNT_TYPE': '00',
            'ACCOUNT_NO': '6227001447170048826',
            'ACCOUNT_NAME': '东东',
            'ACCOUNT_PROP': '0',
            'ID_TYPE': '0',
            'ID': '410621198808081122',
            'REMARK': 'zyw-test',
        },
    }
    print params
    result = tools.send(params)
    print result


def single_pay_verify2():
    """2.6. 账户实名验证(二/三/四要素)
    支持验证卡号，户名，证件，手机号码
    """
    params = {
        'INFO': tools.get_req_info('211004'),
        'VALIDR': {
            'MERCHANT_ID': tools.MERCHANT_ID,
            'SUBMIT_TIME': time.strftime('%Y%m%d%H%M%S'),
            # 'BINDID': '',
            # ‘RELATID’: '',
            'BANK_CODE': '0105',
            'ACCOUNT_TYPE': '00',  # 00银行卡，01存折，02信用卡。不填默认为银行卡00。
            'ACCOUNT_NO': '6227001447170048826',
            'ACCOUNT_NAME': '东东',
            'ACCOUNT_PROP': '0',
            'ID_TYPE': '0',  # 0：身份证,1: 户口簿，2：护照,3.军官证,4.士兵证，5. 港澳居民来往内地通行证,6. 台湾同胞来往内地通行证,7. 临时身份证,8. 外国人居留证,9. 警官证, X.其他证件
            'ID': '410621198808081024',
            # 'RELATEDCARD': '',
            # 'TEL': '',
            # 'MERREM': '',
            'REMARK': 'zyw-test',
        },
    }
    print params
    result = tools.send(params)
    print result


def single_pay_verify3():
    """2.7. 账户实时签约(四要素)
    验证卡号，户名，证件，手机号码，并且生成代收协议
    """
    params = {
        'INFO': tools.get_req_info('211005'),
        'VALIDR': {
            'MERCHANT_ID': tools.MERCHANT_ID,
            'SUBMIT_TIME': time.strftime('%Y%m%d%H%M%S'),
            # 'BINDID': '',
            # ‘RELATID’: '',
            'BANK_CODE': '0105',  # 银行代码，见附录4.3
            'ACCOUNT_TYPE': '00',  # 00银行卡，01存折，02信用卡。不填默认为银行卡00。
            'ACCOUNT_NO': '6227001447170048826',  # 账号银行卡或存折号码
            'ACCOUNT_NAME': '东东',  # 银行卡或存折上的所有人姓名。
            'ACCOUNT_PROP': '0',  # 0私人，1公司。不填时，默认为私人0。
            'ID_TYPE': '0',  # 0：身份证,1: 户口簿，2：护照,3.军官证,4.士兵证，5. 港澳居民来往内地通行证,6. 台湾同胞来往内地通行证,7. 临时身份证,8. 外国人居留证,9. 警官证, X.其他证件
            'ID': '410621198808081024',
            # 'RELATEDCARD': '',
            'TEL': '18888888888',  # 手机号/小灵通
            # 'MERREM': '',    # 商户保留信息
            'REMARK': 'zyw-test',  # 供商户填入参考信息。若为信用卡，填有效期
        },
    }
    print params
    result = tools.send(params)
    print result


def single_pay_apply():
    """2.8. 实名付申请
    验证卡号，户名，证件，手机号码，短信验证码，验证生成生成代收协议，需接口代收接口一并使用
申请有效时间为2小时
    """
    params = {
        'INFO': tools.get_req_info('211006'),
        'RNPA': {
            'MERCHANT_ID': tools.MERCHANT_ID,
            'BANK_CODE': '0105',  # 银行代码，见附录4.3
            'ACCOUNT_TYPE': '00',  # 00银行卡，01存折，02信用卡。不填默认为银行卡00。
            'ACCOUNT_NO': '6227001447170048826',  # 账号银行卡或存折号码
            'ACCOUNT_NAME': '东东',  # 银行卡或存折上的所有人姓名。
            'ACCOUNT_PROP': '0',  # 0私人，1公司。不填时，默认为私人0。
            'ID_TYPE': '0',  # 0：身份证,1: 户口簿，2：护照,3.军官证,4.士兵证，5. 港澳居民来往内地通行证,6. 台湾同胞来往内地通行证,7. 临时身份证,8. 外国人居留证,9. 警官证, X.其他证件
            'ID': '410621198808081024',
            'TEL': '18888888888',  # 手机号/小灵通
            # 'MERREM': '',    # 商户保留信息
            'REMARK': 'zyw-test',  # 供商户填入参考信息。若为信用卡，填有效期
        },
    }
    print params
    result = tools.send(params)
    info, rnparet = result['INFO'], result['RNPARET']
    if info['RET_CODE'] == '0000':
        pass
    print result


def single_pay_send_sms():
    """2.9. 实名付短信重发
    """
    params = {
        'INFO': tools.get_req_info('211006R'),
        'RNPR': {
            'MERCHANT_ID': tools.MERCHANT_ID,
            'SRCREQSN': '',  # 对应申请请求报文中的REQ_SN
        },
    }
    print params
    result = tools.send(params)
    info, RNPRRET = result['INFO'], result['RNPRRET']
    if info['RET_CODE'] == '0000':
        pass
    print result


def single_pay_verify_code():
    """2.10. 实名付确认
    短信确认次数不能超过5次(不含5次) ，后续可能会根据业务发展做调整
验证码有效时间为20分钟
    """
    params = {
        'INFO': tools.get_req_info('211006C'),
        'RNPC': {
            'MERCHANT_ID': tools.MERCHANT_ID,
            'SRCREQSN': '',  # 对应申请请求报文中的REQ_SN
            'VERCODE': '',  # 短信验证码
        },
    }
    print params
    result = tools.send(params)
    info, RNPC = result['INFO'], result['RNPC']
    if info['RET_CODE'] == '0000':
        pass
    print result


def single_pay_query_result():
    """2.11. 实名付结果查询
    """
    params = {
        'INFO': tools.get_req_info('211006Q'),
        'RNPR': {
            'MERCHANT_ID': tools.MERCHANT_ID,
            'SRCREQSN': '',  # 对应申请请求报文中的REQ_SN
        },
    }
    print params
    result = tools.send(params)
    info, RNP = result['INFO'], result['RNP']
    if info['RET_CODE'] == '0000':
        pass
    print result


def single_pay_verify_and_send_sms():
    """2.12. 账户实名验证(四要素+短信)申请
    """
    params = {
        'INFO': tools.get_req_info('211007'),
        'RNPA': {
            'MERCHANT_ID': tools.MERCHANT_ID,
            'BANK_CODE': '0105',  # 银行代码，见附录4.3
            'ACCOUNT_TYPE': '00',  # 00银行卡，01存折，02信用卡。不填默认为银行卡00。
            'ACCOUNT_NO': '6227001447170048826',  # 账号银行卡或存折号码
            'ACCOUNT_NAME': '东东',  # 银行卡或存折上的所有人姓名。
            'ACCOUNT_PROP': '0',  # 0私人，1公司。不填时，默认为私人0。
            'ID_TYPE': '0',  # 0：身份证,1: 户口簿，2：护照,3.军官证,4.士兵证，5. 港澳居民来往内地通行证,6. 台湾同胞来往内地通行证,7. 临时身份证,8. 外国人居留证,9. 警官证, X.其他证件
            'ID': '410621198808081024',
            'TEL': '18888888888',  # 手机号/小灵通
            # 'MERREM': '',    # 商户保留信息
            'REMARK': 'zyw-test',  # 供商户填入参考信息。若为信用卡，填有效期
        },
    }
    print params
    result = tools.send(params)
    info, RNP = result['INFO'], result['RNP']
    if info['RET_CODE'] == '0000':
        pass
    print result


def single_pay_verify_and_send_sms2():
    """2.13. 账户实名验证(四要素+短信)短信重发
    """
    params = {
        'INFO': tools.get_req_info('211007R'),
        'RNPA': {
            'MERCHANT_ID': tools.MERCHANT_ID,
            'SRCREQSN': '',  # 对应申请请求报文中的REQ_SN
        },
    }
    print params
    result = tools.send(params)
    info, RNP = result['INFO'], result['RNP']
    if info['RET_CODE'] == '0000':
        pass
    print result


def single_pay_verify_and_send_sms_conform():
    """2.14. 账户实名验证(四要素+短信)确认
    """
    params = {
        'INFO': tools.get_req_info('211007R'),
        'RNPC': {
            'MERCHANT_ID': tools.MERCHANT_ID,
            'SRCREQSN': '',  # 对应申请请求报文中的REQ_SN
            'VERCODE': '',  # 短信验证码
        },
    }
    print params
    result = tools.send(params)
    info, RNPCRET = result['INFO'], result['RNPCRET']
    if info['RET_CODE'] == '0000':
        pass
    print result


def single_pay_verify_and_send_sms_query_result():
    """2.15. 账户实名验证(四要素+短信)结果查询
    """
    params = {
        'INFO': tools.get_req_info('211007Q'),
        'RNPR': {
            'MERCHANT_ID': tools.MERCHANT_ID,
            'SRCREQSN': '',  # 对应申请请求报文中的REQ_SN
        },
    }
    print params
    result = tools.send(params)
    info, RNP = result['INFO'], result['RNP']
    if info['RET_CODE'] == '0000':
        pass
    print result




if __name__ == '__main__':
    # single_time_verify()
    # single_pay_verify2()
    # single_pay_verify3()
    # single_pay_apply()
    single_pay_verify_and_send_sms_query_result()

