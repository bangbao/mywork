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


# coding: utf-8

import time
import tools


#
# def batch_tranx():
#     """批量代收付接口
#     TRX_CODE:100002--批量代付
#     TRX_CODE:100001--批量代收
#     """
#     params = {
#         'INFO' : {
#             'TRX_CODE' : '100001',
#             'VERSION' : '03',
#             'DATA_TYPE' : '2',
#             'LEVEL' : '6',
#             'USER_NAME' : '20060400000044502',
#             'USER_PASS' : '111111',
#             'REQ_SN' : '200604000000445-dtdrtert452352543',
#         },
#         'BODY' : {
#              'TRANS_SUM' : {
#                 'BUSINESS_CODE' : '10600',
#                 'MERCHANT_ID' : '200604000000445',
#                 'SUBMIT_TIME' : '20131218230712',
#                 'TOTAL_ITEM' : '2',
#                 'TOTAL_SUM' : '2000',
#                 'SETTDAY' : '',
#                },
#             'TRANS_DETAILS': {
#                     'TRANS_DETAIL': {
#                           'SN' : '00001',
#                            'E_USER_CODE': '00001',
#                         'BANK_CODE': '0105',
#                         'ACCOUNT_TYPE': '00',
#                         'ACCOUNT_NO': '6225883746567298',
#                         'ACCOUNT_NAME': '张三',
#                         'PROVINCE': '',
#                         'CITY': '',
#                         'BANK_NAME': '',
#                         'ACCOUNT_PROP': '0',
#                         'AMOUNT': '1000',
#                         'CURRENCY': 'CNY',
#                         'PROTOCOL': '',
#                         'PROTOCOL_USERID': '',
#                         'ID_TYPE': '',
#                         'ID': '',
#                         'TEL': '13828383838',
#                         'CUST_USERID': '用户自定义号',
#                         'REMARK': '备注信息1',
#                         'SETTACCT': '',
#                         'SETTGROUPFLAG': '',
#                         'SUMMARY': '',
#                         'UNION_BANK': '010538987654',
#                        },
#                     'TRANS_DETAIL2': {
#                            'SN' : '00002',
#                            'E_USER_CODE': '00001',
#                         'BANK_CODE': '0103',
#                         'ACCOUNT_TYPE': '00',
#                         'ACCOUNT_NO': '6225883746567228',
#                         'ACCOUNT_NAME': '王五',
#                         'PROVINCE': '',
#                         'CITY': '',
#                         'BANK_NAME': '',
#                         'ACCOUNT_PROP': '0',
#                         'AMOUNT': '1000',
#                         'CURRENCY': 'CNY',
#                         'PROTOCOL': '',
#                         'PROTOCOL_USERID': '',
#                         'ID_TYPE': '',
#                         'ID': '',
#                         'TEL': '13828383838',
#                         'CUST_USERID': '用户自定义号',
#                         'REMARK': '备注信息2',
#                         'SETTACCT': '',
#                         'SETTGROUPFLAG': '',
#                         'SUMMARY': '',
#                         'UNION_BANK': '010538987654',
#                        }
#                }
#         },
#     }
#     result = tools.send(params)
#     if result:
#         print  '验签通过，请对返回信息进行处理';
#         # 下面商户自定义处理逻辑，此处返回一个数组
#     else:
#         print("验签结果：验签失败，请检查通联公钥证书是否正确")


def single_cash():
    """单笔实时代收请求
 * 单笔实时接口
 * TRX_CODE:100014--单笔实时代付
 * TRX_CODE:100011--单笔实时代收
    """
    params = {
        'INFO': tools.get_req_info('100011'),
        'TRANS': {
            'BUSINESS_CODE': '19900', #业务代码 附录3.2 '09400',
            'MERCHANT_ID': tools.MERCHANT_ID,
            'SUBMIT_TIME': time.strftime('%Y%m%d%H%M%S'),
            'E_USER_CODE': 'zyw',
            'BANK_CODE': '0102',  # 银行代码，见附录4.3
            'ACCOUNT_TYPE': '00',  # 00银行卡，01存折，02信用卡。不填默认为银行卡00。
            'ACCOUNT_NO': '6212260200047447046',  # 账号银行卡或存折号码
            'ACCOUNT_NAME': '张彦伟',  # 银行卡或存折上的所有人姓名。
            'ACCOUNT_PROP': '0',  # 0私人，1公司。不填时，默认为私人0。
            'ID_TYPE': '0',  # 0：身份证,1: 户口簿，2：护照,3.军官证,4.士兵证，5. 港澳居民来往内地通行证,6. 台湾同胞来往内地通行证,7. 临时身份证,8. 外国人居留证,9. 警官证, X.其他证件
            'ID': '410621198705131076',   # 证件号
            'TEL': '18910437238',  # 手机号/小灵通
            'AMOUNT': '1',
            'CURRENCY': 'CNY',
            'CUST_USERID': 'zyw',
            'SUMMARY': 'zyw-test',
            # 'MERREM': '',    # 商户保留信息
            'REMARK': 'zyw-test',  # 供商户填入参考信息。若为信用卡，填有效期
        },
    }
    print params
    result = tools.send(params)
    print result
    if result:
        print '验签通过，请对返回信息进行处理'
        # 下面商户自定义处理逻辑，此处返回一个数组
    else:
        print "验签结果：验签失败，请检查通联公钥证书是否正确"
    print result


def query_ret():
    """交易结果查询
    """
    params = {
        'INFO': {
            'TRX_CODE': '200004',
            'VERSION': '03',
            'DATA_TYPE': '2',
            'LEVEL': '6',
            'USER_NAME': tools.USER_NAME,
            'USER_PASS': tools.USER_PASS,
            'REQ_SN': tools.get_req_sn(),
        },
        'QTRANSREQ': {
            'QUERY_SN': '200604000000445-1502964826-000000',
            'MERCHANT_ID': tools.MERCHANT_ID,
            'STATUS': '2',
            'TYPE': '1',
            'START_DAY': '',
            'END_DAY': ''
        }
    }
    result = tools.send(params)
    print result


# coding: utf-8

from lib import tools


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


if __name__ == '__main__':
    # realname_pay_apply()
    #realname_pay_verify_code('200290000018088-20170818131215-000000', '4023')
    realname_pay_result('200290000018088-20170818131215-000000')
    # query_ret()
    single_cash()
    # batch_tranx()