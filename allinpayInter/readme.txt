�����̻��ţ�200604000000445
�û���20060400000044502
���룺  `12qwe  ��֤������111111��
���Խ��׷��͵�ַ��https://113.108.182.3/aipg/ProcessServlet 
�����ֹ����½���״̬����򿪵�ַ��http://113.108.182.3:8083/apptest/updateRet.jsp
webǰ�˽��ײ�ѯ��ַ��http://113.108.182.3/aiap
web���û�����20060400000044502
       �û����룺`12qwe
����֤���總��
����demo�總����php_demo.zip

/*
ͨ�����Ե�ַ��https://113.108.182.3/aipg/ProcessServlet
�Լ�����������ַ: https://tlt.allinpay.com/aipg/ProcessServlet

����˽Կ
openssl genrsa -out rsa_private_key.pem 1024
���ɹ�Կ
openssl rsa -in rsa_private_key.pem -pubout -out rsa_public_key.pem


ת��˽Կ
openssl pkcs12 -nocerts -nodes -in 20060400000044502.p12 -out 20060400000044502.pem

ת����ʱ�������ǣ�111111

ת����Կ(��֤��)
openssl x509 -inform DER -in allinpay-pds.cer  -out allinpay-pds.pem

�洢�ʹ����xml��utf-8�����͵�Զ��ת��� GBK��Զ�̷�������ת����utf-8

��Ҫ֧�ֵ���չ�У�
cURL
OpenSSL
SimpleXML
XMLReader
mbstring
���PHP�汾���� php 5.4.1 ������ hextobin ��� hex2bin ����
*/