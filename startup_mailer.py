import subprocess
import smtplib
import socket
from email.mime.text import MIMEText
import datetime
# Change to your own account information
to = 'kunguz@gmail.com'
gmail_user = 'opticalmicrosystemslaboratory@gmail.com'
gmail_password = 'a1b2c3d4e5f6g7'
smtpserver = smtplib.SMTP('smtp.gmail.com', 587)
smtpserver.ehlo()
smtpserver.starttls()
smtpserver.ehlo
smtpserver.login(gmail_user, gmail_password)
today = datetime.date.today()
# Very Linux Specific
arg='ip route list'
p=subprocess.Popen(arg,shell=True,stdout=subprocess.PIPE)
data = p.communicate()
split_data = data[0].split()
ipaddr = split_data[split_data.index('src')+1]
my_ip = 'IP address of %s is %s' %  (socket.gethostname(),ipaddr)
msg = MIMEText(my_ip)
msg['Subject'] = 'IP For %s on %s' % (socket.gethostname(),today.strftime('%b %d %Y'))
msg['From'] = gmail_user
msg['To'] = to
smtpserver.sendmail(gmail_user, [to], msg.as_string())
smtpserver.quit()

