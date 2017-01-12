#/bin/bash
alias arg1=$1

git clone https://github.com/postgres/postgres.git
cd postgres/config
make
cd ../..
curl -O http://mirror.metrocast.net/apache//httpd/httpd-2.4.25.tar.gz
gzip -d httpd-2.4.25.tar.gz
tar xvf httpd-2.4.25.tar.gz
cd httpd-2.4.25.tar.gz
./configure --prefix=arg1
make
make install
arg1/bin/apachectl -k start # testing

