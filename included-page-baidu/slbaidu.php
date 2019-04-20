<?php

header("Content-type:text/html;charset=utf-8");

$root_path = dirname(__FILE__);
$path_yuming = $root_path .'/' .'yuming';
$path_result = $root_path .'/' .'jieguo.txt';

$total_domains = 0; //总域名
$included_domains = 0; //总收录域名

$handler_dir = scandir($path_yuming);
$total_files = count($handler_dir) - 2; //总文件数

if(isset($_GET["type"])) {
    if($_GET["type"] == "init") {
        $domains = [];
        $list_files = scandir($path_yuming);
        foreach($list_files as $f_name) {
            if($f_name != '.' && $f_name != '..') {
                $tmp['name'] = $f_name;
                $tmp['dlist'] = file($path_yuming .'/' .$f_name);
                $domains[]= $tmp;
            }
        }       
        echo json_encode($domains);
    }
    if($_GET["type"] == "query") {
        $domain = $_GET["domain"];
        echo file_get_contents("https://api.qqsuu.net/api/site?url=fangbianqi.tw");
    }
}



?>