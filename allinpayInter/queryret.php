<?php
/**
 * 交易结果查询 200004
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
        'TRX_CODE' => '200004',
        'VERSION' => '03',
        'DATA_TYPE' => '2',
        'LEVEL' => '6',
        'USER_NAME' => '20060400000044502',
        'USER_PASS' => '111111',
        'REQ_SN' => '200604000000445-rrrr1356732135xxxx',
    ),
    'QTRANSREQ' => array(
        'QUERY_SN' => '22222222222222222222222',
        'MERCHANT_ID' => '200604000000445',
        'STATUS' => '2',
        'TYPE' => '1',
        'START_DAY' => '',
        'END_DAY' => ''
    ),
);
//发起请求
$result = $tools->send( $params);
print_r($result);