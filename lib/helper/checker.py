# coding: utf-8


def check_phone(phone):
    """检测手机号是否符合规范
    现只对国内手机号
    Args:
        phone: 手机号
    Returns:
        bool值: 是否通过校验
    """
    if not phone:
        return False
    if not phone.isdigit():
        return False
    if len(phone) != 11:
        return False
    return True