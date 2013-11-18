#!/usr/bin/python
# -*- coding: utf-8 -*-

__author__ = ('Kaan Akşit')

import sys,os,time,pygame,socket,csv
from pygame.locals import *

# Read image 

# Main loop
def main():
    # Open a socket to read CSV.
    ifile   = open("offsets.csv", "rb")
    reader  = csv.reader(ifile)
    # Get every line in the CSV file.  
    lines = [l for l in reader]
    # Close the socket.
    ifile.close()
    print lines   
    writer = csv.writer(open('output.csv', 'w'))
    writer.writerows(lines)
    return True

if __name__ == '__main__':
    sys.exit(main())
