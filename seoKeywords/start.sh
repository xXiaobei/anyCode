#!/bin/bash

# 主关键词
main_keywords=""
# 过滤关键词或短语
filter_keywords=""
# 必须包含关键词
includ_keywords=""
# 保存关键词的文件名
save_file_name=""

echo "------------------------------------------------"
echo " "
echo " 百度m端挖词 By tz@peiqi ver=1.0"
echo " "
echo "------------------------------------------------"
echo -e " 主关键词：\033[31m必须条件\033[0m，本次挖词中所有的关键词会从主关键词的相关词，其他人还搜词衍生而来"
echo -e " 过滤词（短语）：非必须条件，本次挖词中所有的关键都不会包含过滤词，\033[31m多个词用【英文逗号】分隔\033[0m"
echo -e " 包含词（短语）：非必须条件，本次挖词中所有的关键词必须包含的词或短语，\033[31m多个词用【英文逗号】分隔\033[0m"
echo "------------------------------------------------"
echo -e " \033[31m注意\033[0m：非必须条件可以提升关键词挖掘质量，建议配置"
echo -e "       程序每次运行，会创建 \033[34m/home/documents/seobaidu/baiduci/【主关键词】.txt\033[0m， "
echo "       用于保存采集到的有效关键词。"
echo "------------------------------------------------"
echo -e " \033[34m提示\033[0m： 若输入过程中出错，或想重来，请依次按键 \033[34mCtrl+z\033[0m"
echo "------------------------------------------------"

while [ -z ${main_keywords} ]
do
    read -p "请输入本次挖词的主关键词：" main_keywords
    if [[ -n "$main_keywords" ]];then
        break
    fi
done

read -p "请输入过滤词（短语）：" filter_keywords
read -p "请输入包含词（短语）：" includ_keywords

#echo ${main_keywords}" "${filter_keywords}" "${includ_keywords}

python appMobile.py ${main_keywords} ${filter_keywords} ${includ_keywords}