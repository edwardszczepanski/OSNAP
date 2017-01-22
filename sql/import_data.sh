#! usr/bin/bash

curl -O https://classes.cs.uoregon.edu//17W/cis322/files/osnap_legacy.tar.gz
tar -xvf osnap_legacy.tar.gz
rm osnap_legacy.tar.gz
cd osnap_legacy
rm .*.csv
cd ..
# Do some cool stuff here
rm -rf osnap_legacy
