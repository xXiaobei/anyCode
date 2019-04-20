<?php

/*
 # linux服务器下 精品站案例建站
 # 案例站的数据库为 dbdemo
 # 案例站的根目录为 /home/wwwroot/demo.com
 # /home/wwwroot目录下放置配置文件 config.txt utf-8 编码
 # 注意：
 # 案例数据库的权限 给777 ，data目录权限777 ，完成后恢复为755 ，并删除案例数据库
 # 配置文件，配置文件目录 给权限777 ，完成后恢复原有权限，并删除案例配置文件 vhost 默认600 panel 默认600 server 755 www755
 # /home/wwwroot 配置为777权限，完成后恢复为 755
*/

header("Content-type: text/html; charset=utf-8"); 

echo ' <p>============================================================================</p>
		    <p>#：请确保路径 /www/server/data/ 已赋值777权限</p>
		    <p>#：请确保路径 /www/server/data/dbdemo 下的所有文件已经赋值777权限</p>
			<p>#：请确保路径 /www/server/panel/vhost/nginx/ 已赋值777权限</p>
			<p>#：请确保路径 /home/wwwroot/ 已经赋值777权限</p>
			<p>##：在设置好以上权限后，请运行 start.sh 初始所有相关文件的权限</p>
			<p>##：结束安装后 请执行 find -name "web.php" | xargs rm -rf 删除所有目录中的 web.php (网站安装文件）</p>
			<p>##：结束安装后，请执行 end.sh 恢复所有相关目录的初始权限</p>
			<p>============================================================================ </p>';

//文件夹复制
function copydir($source, $dest) {
    if (!file_exists($dest)) mkdir($dest);
    $handle = opendir($source);
    while (($item = readdir($handle)) !== false) {
        if ($item == '.' || $item == '..') continue;
        $_source = $source . '/' . $item;
        $_dest = $dest . '/' . $item;
        if (is_file($_source)) copy($_source, $_dest);
        if (is_dir($_source)) copydir($_source, $_dest);
    }
    closedir($handle);
}	

$rootPath =  dirname(__FILE__);
$confSite = file(dirname($rootPath) . '/'. 'config.txt');
//$rootpwd = file_get_contents($rootPath . '/'. 'root.txt');

$confSplit = '	';

$resSQLS='';

if(!isset($confSite)) {
	echo '<hr>';
	die("网站配置文件获取错误，请检查");
}

//检查数据库目录权限
if(!mkdir('/www/server/data/t_t_t/',0777,true)){
	die("数据库目录：/www/server/data/ ". "无法写入文件，请赋值777权限。");
}else {
	//检查案例站数据库文件是否能读取	
	if(!copy('/www/server/data/dbdemo/dede_addonarticle.MYD','/www/server/data/t_t_t/dede_addonarticle.MYD')){
			rmdir('/www/server/data/t_t_t/');
			die("案例站数据库dbdemo中的文件不能被复制，请将dbdemo所有文件赋值777权限。");
	}else{
		unlink('/www/server/data/t_t_t/dede_addonarticle.MYD');
		rmdir('/www/server/data/t_t_t/');	
	}	
}

//检查网站配置目录权限
if(!mkdir('/www/server/panel/vhost/nginx/t_t_t/',0777,true)){
	die("网站配置目录：/www/server/panel/vhost/nginx/ 无法写入文件，请赋值777权限。");
}else {
	rmdir('/www/server/panel/vhost/nginx/t_t_t/');
}

//检查网站根目录权限
if(!mkdir('/home/wwwroot/t_t_t/',0777,true)){
	die('网站文件无法被复制，请检查/home/wwwroot 是否已赋值777权限。');
}else {
	rmdir('/home/wwwroot/t_t_t/');
}	


foreach($confSite as $v) {
	$aryTmp = explode($confSplit, $v);
	
	if(isset($aryTmp)) {		
		$siteName = $aryTmp[0];
		$siteTitle = $aryTmp[1];
		$siteKeywords = $aryTmp[2];
		$siteDescription = $aryTmp[3];
		$siteBeian = $aryTmp[4];
		
		//替换域名中的特殊字符
		$refuseStr = array(".","-");//特殊字符数组
		$dbName = str_replace($refuseStr, '_', $siteName);
		
		//数据库名长度不能超过16位
		if(strlen($dbName > 16)) {
			$dbName = substr($dbName, 0, 14);
		}
		
		$siteUrl = "";
		if(!strpos($siteName, 'www.')) {
			$siteUrl = 'http://www.' .$siteName;
		}
		
		//网站配置更改sql语句
		$resSQLS .= 'update '. $dbName .'.dede_sysconfig set value="'.$siteUrl.'" where varname="cfg_basehost";<br />';
		$resSQLS .= 'update  '. $dbName .'.dede_sysconfig set value="'.$siteTitle.'" where varname="cfg_webname";<br />';
		$resSQLS .= 'update  '. $dbName .'.dede_sysconfig set value="'.$siteKeywords.'" where varname="cfg_keywords";<br />';
		$resSQLS .= 'update  '. $dbName .'.dede_sysconfig set value="'.$siteBeian.'" where varname="cfg_description";<br />';
		
		//复制数据库
		echo '<hr>';
		echo '>>> 正在为网站：'.$siteName.' 创建名为：'.$dbName.' 的数据库 <br />';
		$dbPath = '/www/server/data/'. $dbName;
		if(!mkdir($dbPath,0755,true)) {          
			echo $siteName.' 数据库 '.$dbName .'创建失败...';
			continue;
		}
		$dbSource = opendir('/www/server/data/dbdemo/');
		while(false !== ($file = readdir($dbSource))) {
			if($file != '.' && $file != '..') {
				copy('/www/server/data/dbdemo/'.$file, '/www/server/data/'.$dbName.'/'.$file);
			}
		}
		echo '>>>  数据库：'.$dbName.' 创建成功 <br />'; 
		
		//创建网站配置文件
		echo '>>> 正在为网站：'. $siteName. '创建配置文件 <br />';
		$rcPath = '/www/server/panel/vhost/nginx/';
		$defConf = $rcPath . 'demo.com.conf';		
		$btRewrite = '/www/server/panel/vhost/rewrite/'.$siteName. '.conf';
		@file_put_contents($btRewrite,'');//宝塔面板重写规则		
		$curConf = $rcPath . $siteName. '.conf';
		$fc = file($defConf);//读取默认配置文件内容
            
		if(isset($fc)) {			
			$str301 = '
				#301-START
					if ($host ~ \'^'.$siteName.'\'){
						return 301 http://www.'.$siteName.'$request_uri;
					}
				#301-END';
			$fc[3] = 'server_name ' .$siteName .' ' .'www.'.$siteName . ' ' .'m.'.$siteName.';'."\n";
			$fc[5] = "\n".'root /home/wwwroot/' .$siteName .';' .$str301. "\n";
            //$resconf = iconv('gbk','utf-8', implode('',$fc));
			@file_put_contents($curConf,implode('',$fc));//写配置文件内容			
		}
		echo '>>> 配置文件：' .$curConf . ' 写入成功<br />';
      
		//复制案例网站内容
		echo '>>> 正在复制案例站的文件到 网站：'. $siteName. ' 中... <br />';
		$srcPath = '/home/wwwroot/demo.com';
		$destPath = '/home/wwwroot/'.$siteName;
        if(!mkdir($destPath,0777,true)) {
        	echo '>>> 网站：'.$siteName .' 根目录创建失败！';
          	continue;
        }
		copydir($srcPath, $destPath);
      
		//修改网站数据配置文件、网站缓存配置文件
        $pdbConf = '/home/wwwroot/' . $siteName . '/data/common.inc.php';
      	$sitedbConf = file($pdbConf);
        if(isset($sitedbConf)) {
          $sitedbConf[4] = '$cfg_dbname = \''. $dbName .'\';'."\n";
          @file_put_contents($pdbConf,implode('',$sitedbConf));
        }
		
      	$psiteConf = '/home/wwwroot/' . $siteName . '/data/config.cache.inc.php';
        $siteCachConf = file($psiteConf);
        if(isset($siteCachConf)) {
          $siteCachConf[3]= '$cfg_basehost = \'http://www.'. $siteName .'\';'."\n";
          $siteCachConf[9]= '$cfg_webname = \''.$siteTitle .'\';'."\n";
          $siteCachConf[27]= '$cfg_df_style = \'default\';'."\n";
          $siteCachConf[103]= '$cfg_keywords = \''. $siteKeywords .'\';'."\n";
          $siteCachConf[104]= '$cfg_description = \''. $siteDescription .'\';'."\n";
          $siteCachConf[105]= '$cfg_beian = \''. $siteBeian .'\';'."\n";
          @file_put_contents($psiteConf,implode('',$siteCachConf));
        }	
      
		echo '>>> 网站 ' .$siteName .' 创建完成！';      
	}	
}

echo '<hr>';
echo '更新所有网站的TDK SQL语句... <br />';
echo $resSQLS;

?>