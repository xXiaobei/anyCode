<?php

require '/home/bbei/Documents/Project/anyCode/php/simple_html_dom.php';

function random_baidu_ip()
{
    // 随机获取百度ip
    $ips = array('14.215.178.36',
    '14.215.178.37',
    '112.80.255.162',
    '115.239.217.67',
    '115.239.217.68',
    '115.239.217.68',
    '103.235.46.212',
    '115.239.217.67',
    '61.135.186.217',
    '115.239.217.67',
    '115.239.217.68',
    '111.13.101.232',
    '14.215.178.36',
    '14.215.178.36',
    '115.239.217.67',
    '115.239.217.68',
    '103.235.46.212',
    '220.181.7.234',
    '220.181.7.233',
    '115.239.217.67',
    '61.135.186.218',
    '14.215.178.37', );
    shuffle($ips);

    return $ips[0];
}

function get_suggest_words($words)
{
    //根据关键词获取百度ｍ端下拉，相关，其他词
    $r_ip = random_baidu_ip();
    $search_url = sprintf('http://%s/s?word=%s', $r_ip, urlencode($words));
    $htmls = file_get_html($search_url);

    //相关词
    $kw_xg = [];
    $ret = $htmls->find('div[id=relativewords] a');
    //var_dump($ret);
    if ($ret) {
        foreach ($ret as $node) {
            $kw_xg[] = $node->innertext;
        }
    }

    //其他人还搜
    $kw_qt = [];
    $ret = $htmls->find('div[tpl=recommend_list] section a span');
    if (count($ret)) {
        foreach ($ret as $node) {
            $kw_qt[] = $node->innertext;
        }
    }

    //下拉词
    $kw_xl = [];
    $search_url = 'http://m.baidu.com/sugrec?pre=1&p=3&ie=utf-8&json=1&prod=wise&from=wise_web&wd='.urlencode($words);
    $htmls = file_get_contents($search_url);
    if ($htmls) {
        $json = json_decode($htmls);
        foreach ($json->g as $node) {
            $kw_xl[] = $node->q;
        }
    }

    return array(
        'xg' => $kw_xg,
        'qt' => $kw_qt,
        'xl' => $kw_xl,
    );
}

$search_kw = 'vip奥地利探亲访友签证';
//$res_keywords = get_keywords_qtrhs($search_kw);
$kw_sug = get_suggest_words($search_kw);
//var_dump($kw_sug);
