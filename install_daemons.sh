git clone https://github.com/postgres/postgres.git
cd postgres
./configure --prefix=$1
make 
make install

curl -o http-2.4.25 https://archive.apache.org/dist/httpd/httpd-2.4.25.tar.gz
tar -xjf httpd-2.4.25.tar.bz2
cd httpd-2.4.25
./configure --prefix=$1
make
make install
