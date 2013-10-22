echo "Press [CTRL+C] to stop.."
cd /home/pi
while :
do
        sleep 1
        _IP=$(hostname -I) || true
         if [ "$_IP" != "$IP2"  ]; then
             echo $_IP
             echo $IP2 
             printf "My IP address is %s\n" "$_IP"
             python /home/pi/pi3b/startup_mailer.py > /home/pi/log.txt
         fi
        IP2=$_IP
done
