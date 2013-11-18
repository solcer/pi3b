rm photoaf*
rm Content/photoaf*
wget http://172.20.36.122:8080/photoaf.jpg
cp photoaf.jpg Content/

sudo python adjust_calibrate.py
sudo python screen_update.py $1 $2 $3 $4 $5
