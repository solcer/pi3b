#!/usr/bin/python
# -*- coding: utf-8 -*-

__author__ = ('Kaan Akşit')

import sys,os,time

# Function to update screens.
def UpdateScreen(tty=6,ImagePath='./Content/blank.png'):
    command = 'fbi -T %s %s --autozoom --noverbose' % (tty,ImagePath)
    os.system(command)
    return True

# Function to assign TTYs to found framebuffer devices.
def AssignTtysToScreens(ScreenList):
    TtyList = []
    del TtyList[:]
    for i in xrange(0,len(ScreenList)):
        tty = '%s' % (i+10)
        TtyList.append(tty)
        command = './con2fb %s %s' % (ScreenList[i],TtyList[i])
        print command
        os.system(command) 
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
    # Finding the screens connected to the device.
    print '\nFramebuffer devices found:'
    screens = FindScreens()
    print screens
    # Assigning TTY to each framebuffer device.
    print '\nAssigned TTY values for found Framebuffer devices:'
    ttys    = AssignTtysToScreens(screens)
    print ttys
    # Test pattern is displayed on the each display.
    test(ttys,screens,"no")
    # Each screen is being update with the necessary content.
    # Change the tdelay (secs) to adjust the time in between each screen update.
    tdelay  = 1     
    for i in xrange(0,len(ttys)):
#        UpdateScreen(ttys[i],'./Content/screen%d.png' % (i+1))
        UpdateScreen(ttys[i],'./Content/samplescreen%d.png' % i)
        print 'Updating %s on %s' % (screens[i],ttys[i])
        time.sleep(tdelay)   
    return True

# Display test pattern at each framebuffer device.
def test(ttys,screens,wait="no"):
    print '\nSample Update of screens make sure all of them is displaying logo!'
    for i in xrange(0,len(screens)):
        UpdateScreen(ttys[i])
        print 'Updating %s on %s' % (screens[i],ttys[i])
        if wait == "yes":
            time.sleep(1)
    return True

if __name__ == '__main__':
    sys.exit(main())
