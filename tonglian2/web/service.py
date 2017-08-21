# coding: utf-8

import time
import urllib
import requests
import appconfig
import apputil


def pay():
    """发起支付
    """
    params = {}
    params["cusid"] = appconfig.CUSID    # 平台分配的商户号
    params["appid"] = appconfig.APPID    # 平台分配的APPID
    params["version"] = appconfig.APIVERSION    # 接口版本号
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
    params["sign"] = apputil.sign_array(params,appconfig.APPKEY)  #签名

    url = appconfig.APIURL + "/pay"
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
    params["cusid"] = appconfig.CUSID
    params["appid"] = appconfig.APPID
    params["version"] = appconfig.APIVERSION
    params["trxamt"] = "1"
    params["reqsn"] = "123456788"
    params["oldreqsn"] = "123456"#原来订单号
    params["randomstr"] = "1450432107647"#
    params["sign"] = apputil.sign_array(params,appconfig.APPKEY)#签名

    url = appconfig.APIURL + "/cancel"
    rsp = requests.post(url, params)
    rspArray = rsp.json()
    if validSign(rspArray):
        print "验签正确,进行业务处理"


def  refund():
    """当天交易请用撤销,非当天交易才用此退货接口
    """
    params = {}
    params["cusid"] = appconfig.CUSID
    params["appid"] = appconfig.APPID
    params["version"] = appconfig.APIVERSION
    params["trxamt"] = "1"
    params["reqsn"] = "1234567889"
    params["oldreqsn"] = "123456"#原来订单号
    params["randomstr"] = "1450432107647"#
    params["sign"] = apputil.sign_array(params,appconfig.APPKEY)#签名

    url = appconfig.APIURL + "/refund"
    rsp = requests.post(url, params)
    rspArray = rsp.json()
    if validSign(rspArray):
        print "验签正确,进行业务处理"


def  query():
    """查询订单
    """
    params = {}
    params["cusid"] = appconfig.CUSID
    params["appid"] = appconfig.APPID
    params["version"] = appconfig.APIVERSION
    params["reqsn"] = "123456"
    params["randomstr"] = "1450432107647"#
    params["sign"] = apputil.sign_array(params,appconfig.APPKEY)  #签名

    url = appconfig.APIURL + "/query"
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
        sign =  apputil.sign_array(array, appconfig.APPKEY)
        if sign == signRsp:
            return True
        else:
            print u"验签失败: %s -- %s" % (signRsp, sign)
    else:
        print u"验签失败: %s" % (array['retmsg'])
    return False


if __name__ == '__main__':
    pay()
    # cancel()
    # refund()
    #query()

