# coding: utf-8

import time
from lib import tools
from lib import config
from utils.bank import get_bank_logo_by_name


def realname_pay_apply(account_no, account_name, id_no, tel, bank_code,
                       remark='', account_prop='0', account_type='00',
                       id_type='0'):
    """2.8. 实名付申请
    验证卡号，户名，证件，手机号码，短信验证码，验证生成生成代收协议，需接口代收接口一并使用
申请有效时间为2小时
    """
    params = {
        'INFO': tools.get_req_info('211006'),
        'RNPA': {
            'MERCHANT_ID': config.MERCHANT_ID,
            'BANK_CODE': bank_code,         # 银行代码，见附录4.3
            # 'ACCOUNT_TYPE': account_type,   # 00银行卡，01存折，02信用卡。不填默认为银行卡00。
            'ACCOUNT_NO': account_no,       # 账号银行卡或存折号码
            'ACCOUNT_NAME': account_name,   # 银行卡或存折上的所有人姓名。
            # 'ACCOUNT_PROP': account_prop,   # 0私人，1公司。不填时，默认为私人0。
            'ID_TYPE': id_type,             # 0：身份证,1: 户口簿，2：护照,3.军官证,4.士兵证，5. 港澳居民来往内地通行证,6. 台湾同胞来往内地通行证,7. 临时身份证,8. 外国人居留证,9. 警官证, X.其他证件
            'ID': id_no,                    # 证件号
            'TEL': tel,                     # 手机号/小灵通
            # 'MERREM': '',                 # 商户保留信息
            'REMARK': remark,               # 供商户填入参考信息。若为信用卡，填有效期
        },
    }
    result = tools.send(params)
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
    # assert rnparet['ISSENDSMS'] == '1'
    return True, result


def realname_pay_resend_sms(srcreqsn=''):
    """2.9. 实名付短信重发
    """
    params = {
        'INFO': tools.get_req_info('211006R'),
        'RNPR': {
            'MERCHANT_ID': config.MERCHANT_ID,
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
            'MERCHANT_ID': config.MERCHANT_ID,
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
            'MERCHANT_ID': config.MERCHANT_ID,
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


def single_cash(account_no, account_name, id_no, tel, bank_code, amount,
                remark='', account_prop='0', account_type='00', id_type='0'):
    """单笔实时代收请求
 * 单笔实时接口
 * TRX_CODE:100014--单笔实时代付
 * TRX_CODE:100011--单笔实时代收
    """
    params = {
        'INFO': tools.get_req_info('100011'),
        'TRANS': {
            'BUSINESS_CODE': '19900', #业务代码 附录3.2 '09400',
            'MERCHANT_ID': config.MERCHANT_ID,
            'SUBMIT_TIME': time.strftime('%Y%m%d%H%M%S'),
            'BANK_CODE': bank_code,         # 银行代码，见附录4.3
            # 'ACCOUNT_TYPE': account_type,   # 00银行卡，01存折，02信用卡。不填默认为银行卡00。
            'ACCOUNT_NO': account_no,       # 账号银行卡或存折号码
            'ACCOUNT_NAME': account_name,   # 银行卡或存折上的所有人姓名。
            # 'ACCOUNT_PROP': account_prop,   # 0私人，1公司。不填时，默认为私人0。
            'ID_TYPE': id_type,             # 0：身份证,1: 户口簿，2：护照,3.军官证,4.士兵证，5. 港澳居民来往内地通行证,6. 台湾同胞来往内地通行证,7. 临时身份证,8. 外国人居留证,9. 警官证, X.其他证件
            'ID': id_no,                    # 证件号
            'TEL': tel,                     # 手机号/小灵通
            'AMOUNT': amount,               # 金额, 单位分
            # 'CURRENCY': 'CNY',            # 人民币：CNY, 港元：HKD，美元：USD。不填时，默认为人民币
            # 'CUST_USERID': 'zyw',         # 商户自定义的用户号，开发人员可当作备注字段使用
            # 'SUMMARY': 'zyw-test',        # 交易附言 可空
            # 'MERREM': '',                 # 商户保留信息
            'REMARK': remark,               # 供商户填入参考信息。若为信用卡，填有效期
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


def query_bank_card_bin(acctno):
    """卡bin查询
    """
    params = {
        'INFO': tools.get_req_info('200007'),
        'QCARDBINREQ': {
            'ACCTNO': acctno,   # 卡号
        },
    }
    result = tools.send(params)
    info = result['INFO']
    if info['RET_CODE'] != '0000':
        return False, {'ret_code': info['RET_CODE'],
                       'ret_msg': info['ERR_MSG']}
    rsp = result['QCARDBINRSP']
    data = dict(bank_code=rsp['BANKCODE'],
                bank_name=rsp['ISSNAME'],
                card_type=rsp['CARDTYPE'],
                bank_logo=get_bank_logo_by_name(rsp['ISSNAME']))
    return True, data


def query_ret():
    """交易结果查询
    """
    params = {
        'INFO': tools.get_req_info('200004'),
        'QTRANSREQ': {
            'QUERY_SN': '200604000000445-1502964826-000000',
            'MERCHANT_ID': config.MERCHANT_ID,
            'STATUS': '2',
            'TYPE': '1',
            'START_DAY': '',
            'END_DAY': ''
        }
    }
    result = tools.send(params)
    print result


def notify(request):
    """
    签名原文：64563425345325345|13434245847|245245|745635267|46346346346|345
    签名后的字符串：95d16a9074a1b36438c04a9d0fc98ca6045ad0e596c32ee76df68c0e857f6cd13805dafc1958de1aa2f40c855becfb9e8cfb433bfbd305a993e7a396bd79e54075e4ccdc082f11f9c5b4cf7c776838afd3b2a5982488493fa34851a85a21db2c2aaaecbeada291b68202863aeb0026b98bc9011cccd3c79bcf4d388b65a85afd01eacff76c77031eff2022d683385a87d8b1a1427d7a53dfbca2e805c2048b77e30b0b46f0a3e04c3d86ede25c36b8f84757fcedb25e6f37c6fca557dccff7d9497d02775dee8d974a264027eda2ca64d0c04eaff7a8adec635e9afe3fbd891fc698c193ad2d0b99880be1b3432682750cf1ee60815edb89f0f86c3b4898594b
    """
    _GET = request.GET
    ACCOUNT_NO = _GET['ACCOUNT_NO']
    MOBILE = _GET['MOBILE']
    AMOUNT = _GET['AMOUNT']
    BATCHID = _GET['BATCHID']
    SETTDAY = _GET['SETTDAY']
    FINTIME = _GET['FINTIME']
    SUBMITTIME = _GET['SUBMITTIME']
    SN = _GET['SN']
    POUNDAGE = _GET['POUNDAGE']
    USERCODE = _GET['USERCODE']
    SIGN = _GET['SIGN']#签名后的字符串

    #print '账号：', ACCOUNT_NO
    #print '手机号：', MOBILE
    #print '交易金额：', AMOUNT
    #print '手续费：', POUNDAGE

    orgstr = '|'.join([ACCOUNT_NO, MOBILE, AMOUNT, BATCHID, SN, POUNDAGE])
    signture=SIGN

    result=tools.verifyStr(orgstr,signture)
    print(result)

    #接收完成记得返回success
    return 'SUCCESS'


def test():
    # realname_pay_apply
    account_no = '6225768730755228'
    account_name = u'张彦伟'
    id_no = '410621198705131076'
    tel = '18910437238'
    retcode, card_info = query_bank_card_bin(account_no)
    bank_code = card_info['bank_code']
    print realname_pay_apply(account_no, account_name, id_no, tel, bank_code)

    #realname_pay_verify_code('200290000018088-20170818131215-000000', '4023')
    # realname_pay_result('200290000018088-20170818131215-000000')
    # query_ret()
    # single_cash()
    # batch_tranx()
    # print query_bank_card_bin('6212260200047447046')
    # print query_bank_card_bin('6225768730755228')


if __name__ == '__main__':
    test()
