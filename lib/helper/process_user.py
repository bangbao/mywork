# -*- coding: utf-8 -*-

from django.conf import settings
from django.contrib.auth.models import User

if settings.IS_SOURCE_CASPAIN:
    from db.models import UserProfile, Employer
else:
    from account.profile import UserProfile, Employer


def setdefault_user_user_type(user):
    """在用户对象上挂载user_type属性
    Args:
        user: 用户对象
    Returns:
        user_type属性
    """
    if not hasattr(user, '_user_type'):
        if UserProfile.objects.filter(user_id=user.id).exists():
            user._user_type = 1
        else:
            user._user_type = 2
    return user._user_type


# 把user_type挂到用户model上
User.user_type = property(setdefault_user_user_type)


def get_create_by(user, need_boss=False):
    """
    集中式: create_by取Auth_User的id,
    分散式: crate_by取Auth_User
    :param user: 用户 UserProfile / Employer
    :param need_boss: 当为子账号时，是否是返回该帐号的主帐号
    :return:
    """
    if need_boss:
        if isinstance(user, Employer):
            user = user.boss.user
    if settings.IS_SOURCE_CASPAIN:
        return user
    elif settings.IS_SOURCE_VOLGA:
        return user.id


def is_profile_user(user):
    """是否主账号
    """
    return user.user_type == 1


def is_employer_user(user):
    """是否子账号
    """
    return user.user_type == 2


def get_user_name(user):
    """获取用户名
    """
    if is_profile_user(user):
        return user.userprofile.name
    elif is_employer_user(user):
        return user.employer.name
    return user.username


def get_profile_user(user):
    """获取主账号user对象
    """
    if is_profile_user(user):
        return user
    return user.employer.boss.user
