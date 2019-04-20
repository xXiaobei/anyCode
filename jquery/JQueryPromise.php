<?php


$host = "199.180.100.233:3306";
$db_user = "dbPeiqi";
$db_pwd = "tz_peiqi@2019";
$db_name = "24436_cn";

$db_con = null;
$msg_ary = array("msg"=>"链接成功！","type"=>"success");

if(isset($_GET["key"])) {
    if($_GET["key"] == "test") {
        $msg_ary["msg"] = "hello,world!";
        $msg_ary["type"] = "success";
        echo json_encode($tmp_ary);
    }
    if($_GET["key"] == "db_init") {        
        if($db_con == null) {            
            $db_con = new mysqli($host,$db_user,$db_pwd,$db_name);
            if(mysqli_connect_error()) {
                $msg_ary["msg"] = "链接失败";
                $msg_ary["type"] = "error";
            }
            echo json_encode($msg_ary);
        }
    }
    if($_GET["key"] == "db_lanmu") {
        if($db_con == null) {
            $db_con = new mysqli($host,$db_user,$db_pwd,$db_name);
        }
        $sql = "SELECT * FROM dede_arctype";
        $res = $db_con->query($sql);
        $msg_ary["msg"] = $res->num_rows;
        echo json_encode($msg_ary);
    }    
    if($_GET['key'] == 'db_sitename') {
        if($db_con == null) {
            $db_con = new mysqli($host,$db_user,$db_pwd,$db_name);
        }
        $sql = "SELECT value FROM dede_sysconfig where varname = 'cfg_webname';";
        $res = $db_con->query($sql);
        $msg_ary["msg"] = $res->fetch_array();
        echo json_encode($msg_ary);
    }
}

?>