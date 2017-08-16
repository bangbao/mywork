<?php
/**
 * 批量代收付接口
 * TRX_CODE:100002--批量代付
 * TRX_CODE:100001--批量代收
 * @var unknown_type
 */
define('ROOT_PATH', './');
require_once ROOT_PATH.'libs/ArrayXml.class.php';
require_once ROOT_PATH.'libs/cURL.class.php';
require_once ROOT_PATH.'libs/PhpTools.class.php';

header('Content-Type: text/html; Charset=UTF-8');
$tools=new PhpTools();
echo '<pre>';
 
// 源数组
$params = array(
    'INFO' => array(
        'TRX_CODE' => '100001',
        'VERSION' => '03',
        'DATA_TYPE' => '2',
        'LEVEL' => '6',
        'USER_NAME' => '20060400000044502',
        'USER_PASS' => '111111',
        'REQ_SN' => '200604000000445-dtdrtert452352543',
    ),
    'BODY' => array(
     	'TRANS_SUM' => array(
	    	'BUSINESS_CODE' => '10600',
	        'MERCHANT_ID' => '200604000000445',
	        'SUBMIT_TIME' => '20131218230712',
	        'TOTAL_ITEM' => '2',
	        'TOTAL_SUM' => '2000',
	        'SETTDAY' => '',
      	 ),
        'TRANS_DETAILS'=> array(
	      	  'TRANS_DETAIL'=> array(
			      	'SN' => '00001',
	      	 		'E_USER_CODE'=> '00001',
					'BANK_CODE'=> '0105',
					'ACCOUNT_TYPE'=> '00',
					'ACCOUNT_NO'=> '6225883746567298',
					'ACCOUNT_NAME'=> '张三',
					'PROVINCE'=> '',
					'CITY'=> '',
					'BANK_NAME'=> '',
					'ACCOUNT_PROP'=> '0',
					'AMOUNT'=> '1000',
					'CURRENCY'=> 'CNY',
					'PROTOCOL'=> '',
					'PROTOCOL_USERID'=> '',
					'ID_TYPE'=> '',
					'ID'=> '',
					'TEL'=> '13828383838',
					'CUST_USERID'=> '用户自定义号',
					'REMARK'=> '备注信息1',
					'SETTACCT'=> '',
					'SETTGROUPFLAG'=> '',
					'SUMMARY'=> '',
					'UNION_BANK'=> '010538987654',
	      		 ),
	      	  'TRANS_DETAIL2'=> array(
	      	 		'SN' => '00002',
	      	 		'E_USER_CODE'=> '00001',
					'BANK_CODE'=> '0103',
					'ACCOUNT_TYPE'=> '00',
					'ACCOUNT_NO'=> '6225883746567228',
					'ACCOUNT_NAME'=> '王五',
					'PROVINCE'=> '',
					'CITY'=> '',
					'BANK_NAME'=> '',
					'ACCOUNT_PROP'=> '0',
					'AMOUNT'=> '1000',
					'CURRENCY'=> 'CNY',
					'PROTOCOL'=> '',
					'PROTOCOL_USERID'=> '',
					'ID_TYPE'=> '',
					'ID'=> '',
					'TEL'=> '13828383838',
					'CUST_USERID'=> '用户自定义号',
					'REMARK'=> '备注信息2',
					'SETTACCT'=> '',
					'SETTGROUPFLAG'=> '',
					'SUMMARY'=> '',
					'UNION_BANK'=> '010538987654',
	      		 )
      	 )
    ),
);
//发起请求
$result = $tools->send( $params);
if($result!=FALSE){
	echo  '验签通过，请对返回信息进行处理';
	//下面商户自定义处理逻辑，此处返回一个数组
}else{
		print_r("验签结果：验签失败，请检查通联公钥证书是否正确");
}
