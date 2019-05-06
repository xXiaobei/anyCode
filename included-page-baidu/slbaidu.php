<?php

header("Content-type:text/html;charset=utf-8");

$root_path = dirname(__FILE__);
$path_yuming = $root_path . '/' . 'yuming';
$path_result = $root_path . '/' . 'jieguo.txt';

$total_domains = 0; //总域名
$included_domains = 0; //总收录域名

$handler_dir = scandir($path_yuming);
$total_files = count($handler_dir) - 2; //总文件数

$mysql_db = null;

if (isset($_GET["type"])) {
    if ($_GET["type"] == "init") {
        $domains = [];
        $list_files = scandir($path_yuming);
        foreach ($list_files as $f_name) {
            if ($f_name != '.' && $f_name != '..') {
                $tmp['name'] = $f_name;
                $tmp['dlist'] = file($path_yuming . '/' . $f_name);
                $domains[] = $tmp;
            }
        }
        echo json_encode($domains);
    }
    if ($_GET["type"] == "query") {
        $domain = $_GET["domain"];
        echo file_get_contents("https://api.qqsuu.net/api/site?url=fangbianqi.tw");
    }
}

if (isset($_GET["type"])) {
    if ($_GET["type"] == "conf") {
        $confs = @file('conf.txt');
        echo json_encode($confs);
    }
    if ($_GET["type"] == "server_info") {
        $server_ip = $_GET["server_ip"];
        $server_user = $_GET["server_user"];
        $server_pwd = $_GET["server_pwd"];

        if ($mysql_db) {
            mysqli_close($mysql_db);
        }

        $mysql_db = mysqli_connect($server_ip . ":3306", $server_user, $server_pwd);
        if (!$mysql_db) {
            $res["msg"] = "数据库连接出错";
            $res["data"] = [];
            echo json_encode($res);
            exit();
        }

        $sql = "SHOW DATABASES;";
        $db_res = $mysql_db->query($sql);
        $res["msg"] = '查询成功';

        while ($row = $db_res->fetch_array()) {
            if ($row['Database'] != 'mysql'
                && $row['Database'] != 'performance_schema'
                && $row['Database'] != 'information_schema') {
                $row_contents[] = $row;
            }
        }

        
        $res["data"] = $row_contents;
        echo json_encode($res);
    }
}
if(isset($_GET["type"])) {
    if ($_GET["type"] == "archives") {
        $res = [];

        $dbName = $_GET["dbName"];
        $server_ip = $_GET["server_ip"];
        $server_user = $_GET["server_user"];
        $server_pwd = $_GET["server_pwd"];

        $mysql_db = mysqli_connect($server_ip . ":3306", $server_user, $server_pwd, $dbName);

        try {
            $del_arctiny = 'DELETE FROM ' . $dbName . '.dede_arctiny where id in (select aid from ' . $dbName . '.dede_addonarticle where length(body) < 10)';
            $issuccess = $mysql_db->query($del_arctiny);

            if ($issuccess) {
                $del_arcaddon = 'delete from ' . $dbName . '.dede_archives where id in (select aid from ' . $dbName . '.dede_addonarticle where length(body) < 10 )';
                $issuccess = $mysql_db->query($del_arcaddon);
                if ($issuccess) {
                    $del_arcmain = 'delete from ' . $dbName . '.dede_addonarticle WHERE length(body) < 10';
                    $issuccess = $mysql_db->query($del_arcmain);
                    if ($issuccess) {
                        $t = mysqli_affected_rows($mysql_db);
                        $res["msg"] = "success";
                        $res["logs"] = $dbName . " 总共清理了 " . $t . " 篇空文章！";
                    }
                }
            }
        } catch (\Throwable $th) {
            $res["msg"] = $_GET["dbName"] . " 数据库删除出错！";
            mysqli_rollback($mysql_db); //数据库事务回滚
        } finally {
        }
        echo json_encode($res);
    }
}