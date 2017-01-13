#!/usr/bin/env bash
export PATH=$1/bin:$PATH
git clone https://github.com/postgres/postgres.git
./postgres/configure --prefix=$1
make world
make install-world
curl -O http://mirror.metrocast.net/apache//httpd/httpd-2.4.25.tar.gz
gzip -d httpd-2.4.25.tar.gz
tar -xvf httpd-2.4.25.tar
cd httpd-2.4.25
./configure --prefix=$1
make
make install
sed -i '/Listen 80/c\Listen 8080' $1/conf/httpd.conf
