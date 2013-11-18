#!/usr/bin/python
# -*- coding: utf-8 -*-

__author__ = ('Kaan Akşit')

import sys,os,time,pygame,socket,csv
from pygame.locals import *

# Main loop
def main():
    # Pico projector number, this determines from which projector it should start calibrating.
    PicopNo    = 0
    # Error margin.
    Error      = 10 
    # Resolution of adjustment, leave it in between 1-10.
    resolution = 1
    # Boundaries of a single slit.
    MinLim     = 1045
    MaxLim     = 1800
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
    while PicopNo < 1:
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
        # Delete and get a new picture from the camera.
        os.system('rm photoaf.*')
        os.system('wget http://172.20.36.122:8080/photoaf.jpg')
        # Read the acquired image from the IP cam.
        image    = pygame.image.load('photoaf.jpg')
        # Threshold the image.
        ThrImage = image.copy()
        pygame.transform.threshold(ThrImage, image, (10,10,10), (140,140,140), (255,255,255), 1)
        # Blob is detected to find out about size and location of the slit.
        mask       = pygame.mask.from_threshold(ThrImage, (255,255,255), (30, 30, 30))
        island     = mask.connected_component()
        BigBlob    = island.get_bounding_rects()[0]
        Min        = BigBlob.top
        Max        = BigBlob.bottom
        SlitHeight = BigBlob.height
        print "Minimum: ", Min, "Maximum: ", Max, "Slit Size in pixels: ", SlitHeight

        # Check if the slit is in the range.
        if Min > MinLim - Error and Min < MinLim + Error:
            if Max > MaxLim - Error and Max < MaxLim + Error:
                PicopNo += 1
                print 'Pico projector No%s is calibrated, moving to the next one.' % PicopNo
        # Change offset to calibrate the picoprojector.
        else:
            # If the slit is closer to the bottom then move it below.
            if Min < MinLim - Error:
               lines[RowNo][2] += resolution
            if Min > MinLim + Error:
               lines[RowNo][2] -= resolution
            if Max < MaxLim - Error:
               lines[RowNo][2] += resolution
            if Max > MaxLim + Error:
               lines[RowNo][2] -= resolution
            if SlitHeight < SlitLim - Error:
               lines[RowNo][4] += resolution
            if SlitHeight > SlitLim + Error:
               lines[RowNo][4] -= resolution
        print "Min deviation: ", Min - MinLim, "Max deviation: ", MaxLim - Max
    # Save the image.
    pygame.image.save(ThrImage, 'output.jpg')
    # Rights the results to the output CSV.
    writer  = csv.writer(open('output.csv', 'w'))
    writer.writerows(lines)
    return True

if __name__ == '__main__':
    sys.exit(main())
