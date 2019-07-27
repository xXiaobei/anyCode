<?php

function get_keywords_qtrhs($search_kw)
{
    //获取百度m端其他人还搜索
    $search_url = 'http://m.baidu.com/s?word='.urlencode($search_kw);
    $search_htmls = @file_get_contents($search_url);

    $pattern = "/<article rl-link-data-xcx=\"false\" rl-link-data-ivk=\"false\" rl-link-data-light=\"false\"([\s\S]*?)>([\s\S]*?)<\/article>/i";
    preg_match_all($pattern, $search_htmls, $res_ary);

    if (count($res_ary) > 0) {
        $search_htmls = $res_ary[0][0];
        $pattern = "/<span([\s\S]*?)>([\s\S]*?)<\/span>/i";
        preg_match_all($pattern, $search_htmls, $res_ary);
        if (count($res_ary) > 0) {
            return array_slice($res_ary[2], 1);
        }
    }
    //当前关键词没有“其他人还搜”相关词，则返回一个空数组[]
    return [];
}

$search_kw = 'vip奥地利探亲访友签证【申根签证】';
$res_keywords = get_keywords_qtrhs($search_kw);
