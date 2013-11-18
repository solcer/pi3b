rm photoaf*
wget http://172.20.36.122:8080/photoaf.jpg

python create_content.py
sudo python screen_update.py 666
sudo python adjust_offsets.py
#sudo python screen_update.py $1 $2 $3 $4 $5
