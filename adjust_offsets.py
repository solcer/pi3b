#!/usr/bin/python
# -*- coding: utf-8 -*-

__author__ = ('Kaan Akşit')

import sys,os,time,pygame,socket,csv
from pygame.locals import *

# Main loop
def main():
    # Recognize Raspberry PI
    if socket.gethostname() == 'PI3B01':
        BlockNumber           = 'a1'
    elif socket.gethostname() == 'PI3B02':
        BlockNumber           = 'a2'
    # Open a socket to read CSV.
    ifile   = open("offsets.csv", "rb")
    reader  = csv.reader(ifile)
    # Get every line in the CSV file.  
    lines   = [l for l in reader]
    # Close the socket.
    ifile.close()
    # Read the acquired image from the IP cam.
    image    = pygame.image.load('photoaf.jpg')
    # Threshold the image.
    ThrImage = image.copy()
    pygame.transform.threshold(ThrImage, image, (10,10,10), (140,140,140), (255,255,255), 1)
    # Average of the each row is calculated.
    ThrCnst = 30
    data    = []
    Max     = 0
    Min     = 0 
    for i in xrange(0,ThrImage.get_height()):
        data.append(0)
        AvgRow = pygame.transform.average_color(ThrImage, pygame.Rect(0, i, ThrImage.get_width(), 1))
        Avg    = AvgRow[0] + AvgRow[1] + AvgRow[2]
        if Avg > ThrCnst:
            data[i] = 1
            if Min == 0:
                Min = i
            Max     = i
    SlitHeight = Max - Min
    print "Minimum: ", Min, "Maximum: ", Max, "Slit Size in pixels: ", SlitHeight
    # Check if the slit is in the range.
    # Error is the error margin in pixels.
    Error   = 10 
    MinLim  = 1100
    MaxLim  = 1790
    SlitLim = 680
    if Min > MinLim - Error and Min < MinLim + Error:
        if Max > MaxLim - Error and Max < MaxLim + Error:
            print "this is ok"
    print "Min deviation: ", Min - MinLim, "Max deviation: ", MaxLim - Max
    # Save the image.
    pygame.image.save(ThrImage, 'output.jpg')
    # Return the image.
    ImgArr  = pygame.PixelArray(image)
    # Rights the results to the output CSV.
    writer  = csv.writer(open('output.csv', 'w'))
    writer.writerows(lines)
    return True

if __name__ == '__main__':
    sys.exit(main())
