#!/usr/bin/python
# -*- coding: utf-8 -*-

__author__ = ('Kaan Akşit')

import sys,os

# Function to update screens.
def UpdateScreen(tty=6,device='/dev/fb0',ImagePath='/home/pi/omllogo.jpg'):
    command = 'fbi -T %s %s %s --autozoom --noverbose' % (tty,device,ImagePath)
    os.system(command)
    return True

# Function to assign TTYs to found framebuffer devices.
def AssignTtysToScreens(ScreenList):
    TtyList = []
    del TtyList[:]
    for i in xrange(0,len(ScreenList)):
        tty = '/dev/tty%s' % (i+6)
        TtyList.append(tty)
        command = './con2fb %s %s' % (ScreenList[i],TtyList[i])
    return TtyList

# Finds the framebuffer devices attached to the system.
def FindScreens():
    ScreenList = []
    del ScreenList[:]
    pipe       = os.popen('ls /dev/fb*')
    for line in pipe.readlines():
        ScreenList.append(line.replace("\n",""))
    return ScreenList

# Main function started when the script is initiated directly.
def main():
    print 'PI3B script, Author(s): %s' % __author__
    print '\nFramebuffer devices found:'
    screens = FindScreens()
    print screens
    print '\nAssigned TTY values for found Framebuffer devices:'
    print AssignTtysToScreens(screens)
    print '\nSample Update of screens make sure all of them is displaying logo!'
    UpdateScreen()
    return True

if __name__ == '__main__':
    sys.exit(main())
