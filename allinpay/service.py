#coding=utf8
"""
阿里 支付宝
"""
import datetime

import realnamepay
import wxpay
from lib import tools, apputil
from lijiang import app


class MissingParameter(Exception):
    """Base Alipay Exception"""


class AllinpayService(object):
    """通连支付
    """
    def _check_params(self, params, names):
        if not all(k in params for k in names):
            raise MissingParameter('missing parameters')

    def verify_notify(self, **data):
        """
        验证回调数据
        :param data: dict
        :return:
        """
        return apputil.valid_sign(data)

    def redirect_to_pay(self, data):
        app.logger.info('redirect_to_pay: %s', data)
        if data.get('name_goods', ''):
            llianpay.default_params['name_goods'] = data.pop('name_goods', '')

        in_para = dict(user_id=data['user_id'],
                       acct_name=data['acct_name'],
                       card_no=data['card_no'],
                       dt_order=datetime.datetime.now().strftime("%Y%m%d%H%M%S"),
                       id_no=data['id_no'],
                       info_order=data['title'],
                       money_order=data['total_fee'],
                       no_order=data['out_trade_no'],
                       risk_item=data['risk_item'])
                       #url_return='http://fdwx.h2ome.cn/bills')
        url = llianpay.create_direct_pay_by_user_url(**in_para)
        return url

    def query_bank_card_bin(self, **data):
        """
        验证回调数据
        :param data: dict
        :return:
        """
        app.logger.info('query_bank_card_bin: %s', data)
        return llianpay.query_bank_card_bin(**data)

    def query_bank_card_bind_list(self, **data):
        """
        验证回调数据
        :param data: dict
        :return:
        """
        app.logger.info('query_bank_card_bind_list: %s', data)
        return llianpay.query_bank_card_bind_list(**data)