# coding: utf-8

import time
from lib import tools


def realname_pay_apply():
    """2.8. 实名付申请
    验证卡号，户名，证件，手机号码，短信验证码，验证生成生成代收协议，需接口代收接口一并使用
申请有效时间为2小时
    """
    params = {
        'INFO': tools.get_req_info('211006'),
        'RNPA': {
            'MERCHANT_ID': tools.MERCHANT_ID,
            'BANK_CODE': '0102',  # 银行代码，见附录4.3
            'ACCOUNT_TYPE': '00',  # 00银行卡，01存折，02信用卡。不填默认为银行卡00。
            'ACCOUNT_NO': '6212260200047447046',  # 账号银行卡或存折号码
            'ACCOUNT_NAME': '张彦伟',  # 银行卡或存折上的所有人姓名。
            'ACCOUNT_PROP': '0',  # 0私人，1公司。不填时，默认为私人0。
            'ID_TYPE': '0',  # 0：身份证,1: 户口簿，2：护照,3.军官证,4.士兵证，5. 港澳居民来往内地通行证,6. 台湾同胞来往内地通行证,7. 临时身份证,8. 外国人居留证,9. 警官证, X.其他证件
            'ID': '410621198705131076',
            'TEL': '18910437238',  # 手机号/小灵通
            # 'MERREM': '',    # 商户保留信息
            'REMARK': 'zyw-test',  # 供商户填入参考信息。若为信用卡，填有效期
        },
    }
    print params
    result = tools.send(params)
    print result
    info = result['INFO']
    # 提交失败
    if info['RET_CODE'] != '0000':
        return False, {'ret_code': info['RET_CODE'],
                       'ret_msg': info['ERR_MSG']}
    # 实名付申请
    rnparet = result['RNPARET']
    if rnparet['RET_CODE'] != '0000':
        return False, {'ret_code': rnparet['RET_CODE'],
                       'ret_msg': rnparet['ERR_MSG']}
    # 是否已发送验证码
    assert rnparet['ISSENDSMS'] == '1'
    return True, result


def realname_pay_resend_sms(srcreqsn=''):
    """2.9. 实名付短信重发
    """
    params = {
        'INFO': tools.get_req_info('211006R'),
        'RNPR': {
            'MERCHANT_ID': tools.MERCHANT_ID,
            'SRCREQSN': srcreqsn,  # 对应申请请求报文中的REQ_SN
        },
    }
    print params
    result = tools.send(params)
    info, rnprret = result['INFO'], result['RNPRRET']
    # 提交失败
    if info['RET_CODE'] != '0000':
        return False, {'ret_code': info['RET_CODE'],
                       'ret_msg': info['ERR_MSG']}
    # 短信重发失败
    if rnprret['RET_CODE'] != '0000':
        return False, {'ret_code': rnprret['RET_CODE'],
                       'ret_msg': rnprret['ERR_MSG']}
    return True, result


def realname_pay_verify_code(srcreqsn, vercode):
    """2.10. 实名付确认
    短信确认次数不能超过5次(不含5次) ，后续可能会根据业务发展做调整
    验证码有效时间为20分钟
    """
    params = {
        'INFO': tools.get_req_info('211006C'),
        'RNPC': {
            'MERCHANT_ID': tools.MERCHANT_ID,
            'SRCREQSN': srcreqsn,  # 对应申请请求报文中的REQ_SN
            'VERCODE': vercode,  # 短信验证码
        },
    }
    print params
    result = tools.send(params)
    print result
    info = result['INFO']
    if info['RET_CODE'] != '0000':
        return False, {'ret_code': info['RET_CODE'],
                       'ret_msg': info['ERR_MSG']}
    rnpcret = result['RNPCRET']
    if rnpcret['RET_CODE'] not in ('0000', '4002'):
        return False, {'ret_code': rnpcret['RET_CODE'],
                       'ret_msg': rnpcret['ERR_MSG']}
    print True, result


def realname_pay_result(SRCREQSN):
    """2.11. 实名付结果查询
    """
    params = {
        'INFO': tools.get_req_info('211006Q'),
        'RNPR': {
            'MERCHANT_ID': tools.MERCHANT_ID,
            'SRCREQSN': SRCREQSN,  # 对应申请请求报文中的REQ_SN
        },
    }
    print params
    result = tools.send(params)
    print
    info = result['INFO']
    if info['RET_CODE'] != '0000':
        return False, {'ret_code': info['RET_CODE'],
                       'ret_msg': info['ERR_MSG']}
    rnp = result['RNP']
    if rnp['RET_CODE'] != '0000':
        return False, {'ret_code': rnp['RET_CODE'],
                       'ret_msg': rnp['ERR_MSG']}
    print True, result


if __name__ == '__main__':
    # realname_pay_apply()
    #realname_pay_verify_code('200290000018088-20170818131215-000000', '4023')
    realname_pay_result('200290000018088-20170818131215-000000')
