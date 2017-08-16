<?php 


class PhpTools{
	 
	
	const certFile = './data/allinpay-pds.pem';//通联公钥证书
	const privateKeyFile = './data/20060400000044502.pem';//商户私钥证书
	const password = '111111';//商户私钥密码以及用户密码
//	const  apiUrl = 'http://172.16.1.11:8080/aipg/ProcessServlet';//通联系统对接请求地址（内网）
	public $arrayXml ;
    const apiUrl = 'http://113.108.182.3:8083/aipg/ProcessServlet';//通联系统对接请求地址（外网,商户测试时使用）
//	const apiUrl = 'https://tlt.allinpay.com/aipg/ProcessServlet';//（生产环境地址，上线时打开该注释）
	
	public function __construct()      
    {      
        $this->arrayXml = new ArrayAndXml();
    }     
	
	/**
	 * PHP版本低于 5.4.1 的在通联返回的是 GBK编码环境使用
	 * 但是本地文件编码是 UTF-8
	 *
	 * @param string $hexstr
	 * @return binary string
	 */
	public function hextobin($hexstr) {
	    $n = strlen($hexstr);
	    $sbin = "";
	    $i = 0;
	
	    while($i < $n) {
	        $a = substr($hexstr, $i, 2);
	        $c = pack("H*",$a);
	        if ($i==0) {
	            $sbin = $c;
	        } else {
	            $sbin .= $c;
	        }
	
	        $i+=2;
	    }
	
	    return $sbin;
	}
	
	/**
	 * 验签
	 */
	public function verifyXml($xmlResponse){
			
		// 本地反馈结果验证签名开始
		$signature = '';
		if (preg_match('/<SIGNED_MSG>(.*)<\/SIGNED_MSG>/i', $xmlResponse, $matches)) {
		    $signature = $matches[1];
		}
		
		$xmlResponseSrc = preg_replace('/<SIGNED_MSG>.*<\/SIGNED_MSG>/i', '', $xmlResponse);
		$xmlResponseSrc1 = mb_convert_encoding(str_replace('<','&lt;',$xmlResponseSrc), "UTF-8", "GBK");
		print_r ('验签原文');
		print_r ($xmlResponseSrc1);
		$pubKeyId = openssl_get_publickey(file_get_contents(PhpTools::certFile));
		$flag = (bool) openssl_verify($xmlResponseSrc, hex2bin($signature), $pubKeyId);
		openssl_free_key($pubKeyId);
	    //echo '<br/>'+$flag;
		if ($flag) {
		    echo '<br/>Verified: <font color=green>Passed</font>.';
		   
		
		    // 变成数组，做自己相关业务逻辑
		    $xmlResponse = mb_convert_encoding(str_replace('<?xml version="1.0" encoding="GBK"?>', '<?xml version="1.0" encoding="UTF-8"?>', $xmlResponseSrc), 'UTF-8', 'GBK');

		    $results = $this->arrayXml->parseString( $xmlResponse , TRUE);
		    echo "<br/><br/><font color=blue>-------------华丽丽的分割线--------------------</font><br/><br/>";
//		    echo $results;
		    return $results;
		} else {
		    echo '<br/>Verified: <font color=red>Failed</font>.';
		    return FALSE;
		}
	}
	
	/**
	 * 验签
	 */
	public function verifyStr($orgStr,$signature){
		echo '签名原文:'.$orgStr;
		$pubKeyId = openssl_get_publickey(file_get_contents(PhpTools::certFile));
		$flag = (bool) openssl_verify($orgStr, hex2bin($signature), $pubKeyId);
		openssl_free_key($pubKeyId);
		
		if ($flag) {
			echo '<br/>Verified: <font color=red>SUCC</font>.';
		    return TRUE;
		} else {
		    echo '<br/>Verified: <font color=red>Failed</font>.';
		    return FALSE;
		}
	}
	
	/**
	 * 签名
	 */
	public function signXml($params){
		 
		$xmlSignSrc = $this->arrayXml->toXmlGBK($params, 'AIPG');
		$xmlSignSrc=str_replace("TRANS_DETAIL2", "TRANS_DETAIL",$xmlSignSrc);
//		echo ($xmlSignSrc);
		$privateKey = file_get_contents(PhpTools::privateKeyFile);
		
		$pKeyId = openssl_pkey_get_private($privateKey, PhpTools::password);
		openssl_sign($xmlSignSrc, $signature, $pKeyId);
		openssl_free_key($pKeyId);
		
		$params['INFO']['SIGNED_MSG'] = bin2hex($signature);
		
		$xmlSignPost = $this->arrayXml->toXmlGBK($params, 'AIPG');

		return  $xmlSignPost;
	}
	/**
	 * 发送请求
	 */
	public function send($params){
		$xmlSignPost=$this->signXml($params);
		$xmlSignPost=str_replace("TRANS_DETAIL2", "TRANS_DETAIL",$xmlSignPost);
		$response = cURL::factory()->post(PhpTools::apiUrl, $xmlSignPost);
	
		if (! isset($response['body'])) {
		    die('Error: HTTPS REQUEST Bad.');
		}
		//获取返回报文
		$xmlResponse = $response['body'];
		print_r("返回报文如下：");
//		print_r(str_replace('<','&lt;',$xmlResponse));
		 //验证返回报文
		$result=$this->verifyXml($xmlResponse);
		return $result;
	}
}

?>