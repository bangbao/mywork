# coding: utf-8

import time
import urllib
import requests
from lib import config
from lib import apputil


def pay():
    """发起支付
    """
    params = {}
    params["cusid"] = config.CUSID  # 平台分配的商户号
    params["appid"] = config.APPID  # 平台分配的APPID
    params["version"] = config.APIVERSION  # 接口版本号
    params["trxamt"] = "1"  # 交易金额 单位为分
    params["reqsn"] =  str(int(time.time()*1000000))     #订单号,自行生成
    params["paytype"] = "W02"  # 交易方式 详见附录3.3 交易方式
    params["randomstr"] = str(int(time.time()))
    params["body"] = "商品名称"  # 订单商品名称，为空则以商户名作为商品名称
    params["remark"] = "备注信息"  # 备注信息
    params['validtime'] = '15'  # 订单有效时间，以分为单位，不填默认为15分钟
    params["acct"] = "o-JEQweC0kSAucr1e2xxhI7pclko"   # 支付平台用户标识 JS支付时使用微信支付-用户的微信openid支付宝支付-用户user_id
    params["limit_pay"] = "no_credit"  # 支付限制 no_credit--指定不能使用信用卡支付
    params["notify_url"] = "http://pay.shuidiguanjia.com/pay-callback-lianlian/"
    params["sign"] = apputil.sign_array(params, config.APPKEY)  # 签名

    url = config.APIURL + "/pay"
    print url
    print params
    resp = requests.post(url, params, timeout=5)
    rspArray = resp.json()
    print rspArray

    # 验签失败
    if not validSign(rspArray):
        return False, {'ret_code': '9999',
                       'ret_msg': u'验签失败'}
    # 通信失败
    if rspArray['retcode'] != 'SUCCESS':
        return False, {'ret_code': rspArray['retcode'],
                       'ret_msg': rspArray['retmsg']}
    # 交易失败
    if rspArray['trxstatus'] != '0000':
        return False, {'ret_code': rspArray['trxstatus'],
                       'ret_msg': rspArray['errmsg']}

    # 交易成功
    return True, rspArray


def  cancel():
    """当天交易用撤销
    """
    params = {}
    params["cusid"] = config.CUSID
    params["appid"] = config.APPID
    params["version"] = config.APIVERSION
    params["trxamt"] = "1"
    params["reqsn"] = "123456788"
    params["oldreqsn"] = "123456"#原来订单号
    params["randomstr"] = "1450432107647"#
    params["sign"] = apputil.sign_array(params, config.APPKEY)  # 签名

    url = config.APIURL + "/cancel"
    rsp = requests.post(url, params)
    rspArray = rsp.json()
    if validSign(rspArray):
        print "验签正确,进行业务处理"


def  refund():
    """当天交易请用撤销,非当天交易才用此退货接口
    """
    params = {}
    params["cusid"] = config.CUSID
    params["appid"] = config.APPID
    params["version"] = config.APIVERSION
    params["trxamt"] = "1"
    params["reqsn"] = "1234567889"
    params["oldreqsn"] = "123456"#原来订单号
    params["randomstr"] = "1450432107647"#
    params["sign"] = apputil.sign_array(params, config.APPKEY)  # 签名

    url = config.APIURL + "/refund"
    rsp = requests.post(url, params)
    rspArray = rsp.json()
    if validSign(rspArray):
        print "验签正确,进行业务处理"


def  query():
    """查询订单
    """
    params = {}
    params["cusid"] = config.CUSID
    params["appid"] = config.APPID
    params["version"] = config.APIVERSION
    params["reqsn"] = "123456"
    params["randomstr"] = "1450432107647"#
    params["sign"] = apputil.sign_array(params, config.APPKEY)  # 签名

    url = config.APIURL + "/query"
    rsp = requests.post(url, params)
    rspArray = rsp.json()
    print rspArray
    if validSign(rspArray):
        print "验签正确,进行业务处理"


def validSign(array):
    """验签
    """
    if array["retcode"] == 'SUCCESS':
        signRsp = array["sign"].lower()
        array["sign"] = ""
        sign = apputil.sign_array(array, config.APPKEY)
        if sign == signRsp:
            return True
        else:
            print u"验签失败: %s -- %s" % (signRsp, sign)
    else:
        print u"验签失败: %s" % (array['retmsg'])
    return False


def notify(request):
    """平台回调通知
    Args:
        appid: 平台分配的APPID
        outtrxid: 收银宝平台流水号通联系统内唯一
        trxcode: 交易类型 见附录3.2
        trxid: 收银宝平台流水号 通联系统内唯一
        trxamt: 交易金额 分为单位
        trxdate: 交易请求日期 yyyyMMdd
        paytime: 交易完成时间 yyyyMMddHHmmss
        chnltrxid: 渠道交易单号 如支付宝,微信平台订单号
        trxstatus: 交易状态 见3.1
        cusid: 商户号
        termno: 终端号
        termbatchid: 终端批次号
        termtraceno: 终端流水号
        termauthno: 终端授权码
        termrefnum: 终端参考号
        trxreserved: 交易备注
        srctrxid: 原交易ID 对于冲正、撤销、退货等交易时填写
        cusorderid: 商户订单号
        acct: 支付人帐号 例如:微信支付的openid 支付宝平台的user_id 如果信息为空,则默认填写000000
        sign: 签名信息
    """
    params = request.POST.dict()

    if apputil.valid_sign(params, config.APPKEY):
        # TODO 此处进行业务逻辑处理
        return 'success'
    return 'erro'


if __name__ == '__main__':
    pay()
    # cancel()
    # refund()
    #query()

