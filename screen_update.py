#!/usr/bin/python
# -*- coding: utf-8 -*-

__author__ = ('Kaan Akşit')

import sys,os

def UpdateScreen(device='/dev/fb0',ImagePath='/home/pi/omllogo.jpg'):
    command = 'fbi -d %s %s --autozoom --noverbose' % (device,ImagePath)
    os.system(command)
    return True

def FindScreens():
    ScreenList = []
    del ScreenList[:]
    pipe       = os.popen('ls /dev/fb*')
    for line in pipe.readlines():
        ScreenList.append(line.replace("\n",""))
    return ScreenList

def main():
    print 'PI3B script, Author(s): %s' % __author__
    print 'Framebuffer devices found:'
    print FindScreens()
    UpdateScreen()
    return True

if __name__ == '__main__':
    sys.exit(main())
