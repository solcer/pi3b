#!/usr/bin/python
# -*- coding: utf-8 -*-

__author__ = ('Kaan Akşit')

import sys,os,time,pygame,socket,csv
from pygame.locals import *

# Main loop
def main():
    # Open a socket to read CSV.
    ifile   = open("offsets.csv", "rb")
    reader  = csv.reader(ifile)
    # Get every line in the CSV file.  
    lines   = [l for l in reader]
    # Close the socket.
    ifile.close()
    # Read images.
    image   = pygame.image.load('photoaf.jpg')
    # Threshold the image.
    pygame.transform.threshold(image, image, color, (0,0,0,0), (0,0,0,0))
    # 
    # Return the image.
    ImgArr  = pygame.PixelArray(image)
    # Rights the results to the output CSV.
    writer  = csv.writer(open('output.csv', 'w'))
    writer.writerows(lines)
    return True

if __name__ == '__main__':
    sys.exit(main())
