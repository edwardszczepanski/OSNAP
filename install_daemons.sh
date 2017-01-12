#/bin/bash

git clone https://github.com/postgres/postgres.git
cd postgres/config
make
cd ../..
curl http://mirror.metrocast.net/apache//httpd/httpd-2.4.25.tar.gz


