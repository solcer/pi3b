sudo pkill fbi
rm ./Content/samplescreen*
python create_content.py
sudo python screen_update.py $1 $2 $3 $4 $5
