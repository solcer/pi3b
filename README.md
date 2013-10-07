Source code for multi-view autostereoscopic display based on pico projectors, and Raspberry Pi boards.

Author(s):

- Kaan Akşit

File descriptions:

- rc.local : to be used as /etc/rc.local in Raspbian.
- ip.sh : Gets the ip value, and initiate automatic ip sending python script.
- startup_mailer.py : A python script to send ip via email.
- con2fb.c : Script to assign TTY to framebuffer devices.

How to make con2fb:

 gcc con2fb.c -o con2fb
