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


if __name__ == '__main__':
    # query_ret()
    single_cash()
    # batch_tranx()