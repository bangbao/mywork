<?php
/*

// Usage:
header('Content-Type: text/html; Charset=UTF-8');
echo '<pre>';

$xmlfile = 'singleRealCashReq.src.tpl.xml';
$arrayXml = new ArrayAndXml();

$output = $arrayXml->parseFile( $xmlfile , TRUE );
print_r($output);

echo '<br><font color=red>-----------------------</font><br>';
$arrayXml->bFormatted = TRUE;

echo htmlspecialchars($arrayXml->toXml($output['AIPG'], 'AIPG'));
*/
/**
 * 本类需要的PHP扩展：XMLReader、simpleXML、DOM (DOM根据情况，如果需要格式化输出XML，就必须加载)
 *
 *
 * 关于属性：本类解析不优化的时候，支持属性；输出XML的时候，不支持属性。
 *
 */
class ArrayAndXml {

    protected $bOptimize = FALSE;

    public $bFormatted = FALSE;

    public function parseString( $sXml , $bOptimize = FALSE) {
        $oXml = new XMLReader();
        $this -> bOptimize = (bool) $bOptimize;
        try {
            // Set String Containing XML data
            $oXml->XML($sXml);

            // Parse Xml and return result
            return $this->parseXml($oXml);
        } catch (Exception $e) {
            echo $e->getMessage();
        }

    }

    public function parseFile( $sXmlFilePath , $bOptimize = false ) {
        $oXml = new XMLReader();
        $this -> bOptimize = (bool) $bOptimize;

        try {
            // Open XML file
            $oXml->open($sXmlFilePath);

            // Parse Xml and return result
            return $this->parseXml($oXml);
        } catch (Exception $e) {
            echo $e->getMessage(). ' | Try open file: '.$sXmlFilePath;
        }
    }

    protected function parseXml( XMLReader $oXml ) {
        $aAssocXML = null;

        $iDc = -1;

        while($oXml->read()){
            switch ($oXml->nodeType) {

                case XMLReader::END_ELEMENT:

                    if ($this->bOptimize) {
                        $this->optXml($aAssocXML);
                    }
                    return $aAssocXML;

                case XMLReader::ELEMENT:

                    if(!isset($aAssocXML[$oXml->name])) {
                        if($oXml->hasAttributes) {
                            $aAssocXML[$oXml->name][] = $oXml->isEmptyElement ? '' : $this->parseXML($oXml);
                        } else {
                            if($oXml->isEmptyElement) {
                                $aAssocXML[$oXml->name] = '';
                            } else {
                                $aAssocXML[$oXml->name] = $this->parseXML($oXml);
                            }
                        }
                    } elseif (is_array($aAssocXML[$oXml->name])) {
                        if (!isset($aAssocXML[$oXml->name][0]))
                        {
                            $temp = $aAssocXML[$oXml->name];
                            foreach ($temp as $sKey=>$sValue)
                                unset($aAssocXML[$oXml->name][$sKey]);
                            $aAssocXML[$oXml->name][] = $temp;
                        }

                        if($oXml->hasAttributes) {
                            $aAssocXML[$oXml->name][] = $oXml->isEmptyElement ? '' : $this->parseXML($oXml);
                        } else {
                            if($oXml->isEmptyElement) {
                                $aAssocXML[$oXml->name][] = '';
                            } else {
                                $aAssocXML[$oXml->name][] = $this->parseXML($oXml);
                            }
                        }
                    } else {
                        $mOldVar = $aAssocXML[$oXml->name];
                        $aAssocXML[$oXml->name] = array($mOldVar);
                        if($oXml->hasAttributes) {
                            $aAssocXML[$oXml->name][] = $oXml->isEmptyElement ? '' : $this->parseXML($oXml);
                        } else {
                            if($oXml->isEmptyElement) {
                                $aAssocXML[$oXml->name][] = '';
                            } else {
                                $aAssocXML[$oXml->name][] = $this->parseXML($oXml);
                            }
                        }
                    }

                    if($oXml->hasAttributes) {
                        $mElement =& $aAssocXML[$oXml->name][count($aAssocXML[$oXml->name]) - 1];
                        while($oXml->moveToNextAttribute()) {
                            $mElement[$oXml->name] = $oXml->value;
                        }
                    }
                    break;
                case XMLReader::TEXT:
                case XMLReader::CDATA:

                    $aAssocXML[++$iDc] = $oXml->value;

            }
        }

        return $aAssocXML;
    }

    public function optXml(&$mData) {
        if (is_array($mData)) {
            if (isset($mData[0]) && count($mData) == 1 ) {
                $mData = $mData[0];
                if (is_array($mData)) {
                    foreach ($mData as &$aSub) {
                        $this->optXml($aSub);
                    }
                }
            } else {
                foreach ($mData as &$aSub) {
                    $this->optXml($aSub);
                }
            }
        }
    }


    public function fixCDATA($string) {
        //fix CDATA tags
        $find[]     = '&lt;![CDATA[';
        $replace[] = '<![CDATA[';
        $find[]     = ']]&gt;';
        $replace[] = ']]>';

        $string = str_ireplace($find, $replace, $string);
        return $string;
    }

    public function is_assoc( $array ) {
        return (is_array($array) && 0 !== count(array_diff_key($array, array_keys(array_keys($array)))));
    }

    public function toXml($data, $rootNodeName = 'data', &$xml=null)
    {
        // turn off compatibility mode as simple xml throws a wobbly if you don't.
        if ( ini_get('zend.ze1_compatibility_mode') == 1 ) ini_set ( 'zend.ze1_compatibility_mode', 0 );
        if ( is_null( $xml ) ) {
            $xml = simplexml_load_string(stripslashes("<?xml version='1.0' encoding='UTF-8'?><$rootNodeName></$rootNodeName>"));
        }

        // loop through the data passed in.
        foreach( $data as $key => $value ) {
 
            // no numeric keys in our xml please!
            $numeric = false;
            if ( is_numeric( $key ) ) {
                $numeric = 1;
                $key = $rootNodeName;
            }

            // delete any char not allowed in XML element names
            $key = preg_replace('/[^a-z0-9\-\_\.\:]/i', '', $key);

            //check to see if there should be an attribute added (expecting to see _id_)
            $attrs = false;

            //if there are attributes in the array (denoted by attr_**) then add as XML attributes
            if ( is_array( $value ) ) {
                foreach($value as $i => $v ) {
                    $attr_start = false;
                    $attr_start = stripos($i, 'attr_');
                    if ($attr_start === 0) {
                        $attrs[substr($i, 5)] = $v; unset($value[$i]);
                    }
                }
            }


            // if there is another array found recursively call this function
            if ( is_array( $value ) ) {
                if ( $this->is_assoc( $value ) || $numeric ) {
                    // older SimpleXMLElement Libraries do not have the addChild Method
                    if (method_exists('SimpleXMLElement','addChild')) {
                        $node = $xml->addChild( $key, null);
                        if ($attrs) {
                            foreach($attrs as $key => $attribute) {
                                $node->addAttribute($key, $attribute);
                            }
                        }
                    }

                }else{
                    $node =$xml;
                }

                // recrusive call.
                if ( $numeric ) $key = 'anon';

                $this->toXml( $value, $key, $node );
            } else {

                // older SimplXMLElement Libraries do not have the addChild Method
                if (method_exists('SimpleXMLElement','addChild')) {
                    $childnode = $xml->addChild( $key, $value);
                    if ($attrs) {
                        foreach($attrs as $key => $attribute) {
                            $childnode->addAttribute($key, $attribute);
                        }
                    }
                }
            }
        }

        if ($this->bFormatted) {
            // if you want the XML to be formatted, use the below instead to return the XML
            $doc = new DOMDocument('1.0');
            $doc->preserveWhiteSpace = false;
            @$doc->loadXML( $this->fixCDATA($xml->asXML()) );
            $doc->formatOutput = true;

            return $doc->saveXML();
        }

        // pass back as unformatted XML
        return $xml->asXML();
    }

    public function toXmlGBK($data, $rootNodeName = 'data', &$xml=null)
    {
        return mb_convert_encoding(str_replace('<?xml version="1.0" encoding="UTF-8"?>', '<?xml version="1.0" encoding="GBK"?>', $this->toXml($data, $rootNodeName, $xml)), 'GBK', 'UTF-8');
    }

}
