# coding: utf-8

import urllib
import requests
import appconfig
import apputil


def pay():
    """发起支付
    """
    params = {}
    params["cusid"] = appconfig.CUSID
    params["appid"] = appconfig.APPID
    params["version"] = appconfig.APIVERSION
    params["trxamt"] = "1"
    params["reqsn"] = "123456"      #订单号,自行生成
    params["paytype"] = "W02"
    params["randomstr"] = "1450432107647"
    params["body"] = "商品名称"
    params["remark"] = "备注信息"
    params["acct"] = "openid"
    params["limit_pay"] = "no_credit"
    params["notify_url"] = "http://pay.shuidiguanjia.com/pay-callback-lianlian/"
    params["sign"] = apputil.sign_array(params,appconfig.APPKEY)  #签名

    url = appconfig.APIURL + "/pay"
    resp = requests.post(url, params, timeout=5)
    rspArray = resp.json()
    if validSign(rspArray):
        print "验签正确,进行业务处理"


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
    params["sign"] = apputil.sign_array(params,appconfig.APPKEY)#签名

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
    #pay()
    # cancel()
    # refund()
    query()

