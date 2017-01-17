#! /bin/bash
export PATH=$1/bin:$PATH

git clone https://github.com/postgres/postgres.git $1
cd $1
./configure --prefix=$1
make
make install

curl -O http://mirror.metrocast.net/apache//httpd/httpd-2.4.25.tar.gz
gzip -d httpd-2.4.25.tar.gz
tar -xvf httpd-2.4.25.tar

cd $1/httpd-2.4.25
./configure --prefix=$1 --with-port-8080
make
make install
