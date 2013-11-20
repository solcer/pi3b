#!/usr/bin/python
# -*- coding: utf-8 -*-

__author__ = ('Kaan Akşit')

import sys,os,time,pygame,socket,csv,time
from pygame.locals import *

# Main loop
def main():
    # If enabled user input offset values.
    ManualMode = 'on'
    # Determines which Picop to calibrate (Device Under Test).
    DUT        = input('Enter the number of the pico projector to calibrate (0-4):')
    # Pico projector number, this determines from which projector it should start calibrating.
    PicopNo    = DUT
    # Error margin.
    Error      = 5
    # Resolution of adjustment, leave it in between 1-10.
    resolution = 10
    # Boundaries of a single slit.
    MinLim     = 1000
    MaxLim     = 1700
    SlitLim    = MaxLim - MinLim
    # Threshold value.
    ThrCnst    = 10
    # Recognize Raspberry PI
    if socket.gethostname() == 'PI3B01':
        BlockNumber           = 'a1'
    elif socket.gethostname() == 'PI3B02':
        BlockNumber           = 'a2'
    # Open a socket to read CSV.
    ifile  = open("offsets.csv", "rb")
    reader = csv.reader(ifile)
    # Get every line in the CSV file.  
    lines  = [l for l in reader]
    # Close the socket.
    ifile.close()
    # Calibrate all the pico projectors one by one via loop.
    while PicopNo == DUT:
        # Free memory from previous session by killing unnecessary programs.
        os.system('sudo pkill fbi')
        # First find the corresponding line in the offset table.
        RowNo = 0
        RowC  = 0
        for elements in lines:
            if elements[0] == BlockNumber and int(elements[1]) == PicopNo:
               RowNo = RowC
            RowC += 1
        # Create the new content according to the new offset table.
        os.system('rm ./Content/samplescreen*')
        os.system('python create_content.py')
        # Only turn on the picop under calibration
        os.system('sudo python screen_update.py %s' % PicopNo)
        time.sleep(2)
        # Delete and get a new picture from the camera.
        os.system('rm photoaf.*')
        os.system('wget http://172.20.36.122:8080/photoaf.jpg')
        # Read the acquired image from the IP cam.
        image    = pygame.image.load('photoaf.jpg')
        # Threshold the image.
        ThrImage = image.copy()
        pygame.transform.threshold(ThrImage, image, (30,30,30), (110,110,110), (255,255,255), 1)
        # Blob is detected to find out about size and location of the slit.
        mask       = pygame.mask.from_threshold(ThrImage, (255,255,255), (30, 30, 30))
        island     = mask.connected_component()
        BigBlob    = island.get_bounding_rects()[0]
        Min        = BigBlob.top
        Max        = BigBlob.bottom
        SlitHeight = BigBlob.height
        print "Minimum: ", Min, "Maximum: ", Max, "Slit Size in pixels: ", SlitHeight

        # Check if the slit is in the range.
        if Min > MinLim - Error and Min < MinLim + Error and  Max > MaxLim - Error and Max < MaxLim + Error and SlitHeight > SlitLim - Error and SlitHeight < SlitLim + Error:
                    PicopNo += 1
                    print 'Pico projector No%s is calibrated, moving to the next one.' % PicopNo
        # Change offset to calibrate the picoprojector.
        else:
            if ManualMode == 'on':
                # Print the new offset values.
                print '\033[92m', lines[RowNo], '\033[0m'
                print '\033[93m', "Min deviation: ", Min - MinLim, "Max deviation: ", MaxLim - Max, "Slit deviation:", SlitHeight - SlitLim, '\033[0m'
                lines[RowNo][2] = input('OffSetLeft (%s):' % lines[RowNo][2])
                lines[RowNo][4] = input('SlitSize (%s):' % lines[RowNo][4])
            else:
                if PicopNo % 2 == 1:
                    m = -1
                else:
                    m = 1
                # If the slit is closer to the bottom then move it below.
                if Min > MinLim + Error:
                    lines[RowNo][2] = int(lines[RowNo][2]) - resolution * m
                if Min < MinLim - Error:
                    lines[RowNo][2] = int(lines[RowNo][2]) + resolution * m
                if Max > MaxLim + Error:
                    lines[RowNo][2] = int(lines[RowNo][2]) - resolution * m
                if Max < MaxLim - Error:
                    lines[RowNo][2] = int(lines[RowNo][2]) + resolution * m
                if SlitHeight > SlitLim + Error:
                    lines[RowNo][4] = int(lines[RowNo][4]) - resolution
                if SlitHeight < SlitLim - Error:
                    lines[RowNo][4] = int(lines[RowNo][4]) + resolution
            # Print the new offset values.
            print '\033[92m', lines[RowNo], '\033[0m'
            # Rights the results to the output CSV.
            f = open('offsets.csv', 'w')
            writer  = csv.writer(f)
            writer.writerows(lines)
            f.close()
        print '\033[93m', "Min deviation: ", Min - MinLim, "Max deviation: ", MaxLim - Max, "Slit deviation:", SlitHeight - SlitLim, '\033[0m'
        # Save the image.
        pygame.draw.rect(ThrImage, (255,0,0), BigBlob, 3)
        pygame.image.save(ThrImage, 'output.jpg')
    return True

if __name__ == '__main__':
    sys.exit(main())
