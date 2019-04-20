#!/bin/bash

rm -rf /home/wwwroot/demo.com/
echo 'success remove Ex site demo.com'
rm -rf /www/server/data/dbdemo/
echo 'success remove Ex db dbdemo'
rm -rf /www/server/panel/vhost/nginx/demo.com.conf
echo 'success remove Ex config demo.com.conf'

find -name 'web.php' /home/wwwroot/ | xargs rm -rf
echo 'success remove web.php in every site'

chmod 755 /www/
echo '/www 755 ch success'
chmod 755 /www/server/
echo '/www/server/ 755 ch success'
chmod 755 /www/server/data/
echo '/www/server/data/ 755 ch success'
chmod 600 /www/server/panel/
echo '/www/server/panel/ 600 ch success'
chmod 600 /www/server/panel/vhost/
echo '/www/server/panel/vhost/ 600 ch success'
chmod 600 /www/server/panel/vhost/nginx/
echo '/www/server/panel/vhost/nginx/ 600 ch success'
chmod -R 755 /home/wwwroot/
echo '/home/wwwroot/ 755 ch success'
