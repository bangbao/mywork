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


if __name__ == '__main__':
    single_time_verify()