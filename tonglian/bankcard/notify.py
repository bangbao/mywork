# coding: utf-8


def notify(reqeust):
    """
    签名原文：64563425345325345|13434245847|245245|745635267|46346346346|345
    签名后的字符串：95d16a9074a1b36438c04a9d0fc98ca6045ad0e596c32ee76df68c0e857f6cd13805dafc1958de1aa2f40c855becfb9e8cfb433bfbd305a993e7a396bd79e54075e4ccdc082f11f9c5b4cf7c776838afd3b2a5982488493fa34851a85a21db2c2aaaecbeada291b68202863aeb0026b98bc9011cccd3c79bcf4d388b65a85afd01eacff76c77031eff2022d683385a87d8b1a1427d7a53dfbca2e805c2048b77e30b0b46f0a3e04c3d86ede25c36b8f84757fcedb25e6f37c6fca557dccff7d9497d02775dee8d974a264027eda2ca64d0c04eaff7a8adec635e9afe3fbd891fc698c193ad2d0b99880be1b3432682750cf1ee60815edb89f0f86c3b4898594b
    """
    _GET = request.GET
    ACCOUNT_NO = _GET['ACCOUNT_NO']
    MOBILE = _GET['MOBILE']
    AMOUNT = _GET['AMOUNT']
    BATCHID = _GET['BATCHID']
    SETTDAY = _GET['SETTDAY']
    FINTIME = _GET['FINTIME']
    SUBMITTIME = _GET['SUBMITTIME']
    SN = _GET['SN']
    POUNDAGE = _GET['POUNDAGE']
    USERCODE = _GET['USERCODE']
    SIGN = _GET['SIGN']#签名后的字符串

    #print '账号：', ACCOUNT_NO
    #print '手机号：', MOBILE
    #print '交易金额：', AMOUNT
    #print '手续费：', POUNDAGE

    orgstr = '|'.join([ACCOUNT_NO, MOBILE, AMOUNT, BATCHID, SN, POUNDAGE])
    signture=SIGN

    result=tools.verifyStr(orgstr,signture)
    print(result)

    #接收完成记得返回success
    return 'SUCCESS'
