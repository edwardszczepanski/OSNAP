#/bin/bash

git clone https://github.com/postgres/postgres.git
cd postgres
./configure --prefix=$1
make
make install
cd ..
curl -O http://mirror.metrocast.net/apache//httpd/httpd-2.4.25.tar.gz
gzip -d httpd-2.4.25.tar.gz
tar xvf httpd-2.4.25.tar
cd httpd-2.4.25
./configure --prefix=$1
make
make install
"arg1/bin/apachectl -k start # testing
sed -i '/Listen 80/c\Listen 8080' $1/conf/httpd.conf
cd ..

export PATH=$1/bin:$PATH
