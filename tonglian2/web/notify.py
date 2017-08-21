# coding: utf-8

import appconfig
import apputil


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

    if apputil.valid_sign(params, appconfig.APPKEY):
        # TODO 此处进行业务逻辑处理
        return 'success'
    return 'erro'
