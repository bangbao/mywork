测试商户号：200604000000445
用户：20060400000044502
密码：  `12qwe  （证书密码111111）
测试交易发送地址：https://113.108.182.3/aipg/ProcessServlet 
若需手工更新交易状态，请打开地址：http://113.108.182.3:8083/apptest/updateRet.jsp
web前端交易查询地址：http://113.108.182.3/aiap
web端用户名：20060400000044502
       用户密码：`12qwe
测试证书如附件
测试demo如附件：php_demo.zip

/*
通联测试地址：https://113.108.182.3/aipg/ProcessServlet
以及生产环境地址: https://tlt.allinpay.com/aipg/ProcessServlet

生成私钥
openssl genrsa -out rsa_private_key.pem 1024
生成公钥
openssl rsa -in rsa_private_key.pem -pubout -out rsa_public_key.pem


转换私钥
openssl pkcs12 -nocerts -nodes -in 20060400000044502.p12 -out 20060400000044502.pem

转换的时候，密码是：111111

转换公钥(或证书)
openssl x509 -inform DER -in allinpay-pds.cer  -out allinpay-pds.pem

存储和处理的xml用utf-8，发送到远程转码成 GBK，远程反馈数据转换成utf-8

需要支持的扩展有：
cURL
OpenSSL
SimpleXML
XMLReader
mbstring
如果PHP版本低于 php 5.4.1 ，请用 hextobin 替代 hex2bin 函数
*/