#! /bin/bash
export PATH=$1/bin:$PATH

git clone -b REL9_5_STABLE https://github.com/postgres/postgres.git $1
cd $1
./configure --prefix=$1
make
make install

curl -O http://mirror.metrocast.net/apache//httpd/httpd-2.4.25.tar.gz
gzip -d httpd-2.4.25.tar.gz
tar -xvf httpd-2.4.25.tar
rm httpd-2.4.25.tar httpd-2.4.25.tar.gz

cd $1/httpd-2.4.25
./configure --prefix=$1
sed -i '/Listen 80/c\Listen 8080' $1/conf/httpd.conf
make
make install
