#!/bin/bash

chmod 777 /www/
echo '/www 777 ch success'
chmod 777 /www/server/
echo '/www/server/ 777 ch success'
chmod 777 /www/server/data/
echo '/www/server/data/ 777 ch success'
chmod -R 777 /www/server/data/dbdemo/
echo 'ex db dbdemo ch 777 success'
chmod 777 /www/server/panel/
echo '/www/server/panel/ 777 ch success'
chmod 777 /www/server/panel/vhost/
echo '/www/server/panel/vhost/ 777 ch success'
chmod 777 /www/server/panel/vhost/nginx/
echo '/www/server/panel/vhost/nginx/ 777 ch success'
chmod 777 /www/server/panel/vhost/nginx/demo.com.conf
echo 'ex config demo.com.conf ch 777 success'
chmod -R 777 /home/wwwroot/
echo '/home/wwwroot/ 777 ch success'
