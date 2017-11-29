# coding: utf-8


class RedisConsts(object):
    """redis key格式定义
    """
    CHECK_PHONE_CODE_COUNT = 'check_phone_code:count:{}'          # 手机号发送验证码次数
    CHECK_PHONE_CODE_TOKEN = 'check_phone_code:token:{}'          # 手机号发送验证码token
    CHECK_PHONE_CODE_CAPTCHA = 'check_phone_code:captcha:{}'      # 手机号对应的验证码
    LIMIT_REQUEST_IP_COUNT = 'limit_request_ip:count:{}'          # 限制IP请求次数
    SINGLE_LIMIT_REQUEST = 'single_limit_request:{}:{}'           # 限制重复请求