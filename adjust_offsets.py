#!/usr/bin/python
# -*- coding: utf-8 -*-

__author__ = ('Kaan Akşit')

import sys,os,time,pygame,socket,csv
from pygame.locals import *

# CSV reader to read offset positions of the pico projectors.
def ReadCSV(filename,BlockNumber):
    # Open a socket to read CSV.
    ifile   = open(filename, "rb")
    reader  = csv.reader(ifile)
    offsets = []
    # Skip header
    next(reader)
    # Read the CSV row by row.
    for row in reader:
        # Avoid empty lines in CSV
        if len(row) > 0:
            # Strip white spaces from CSV file.
            row = ([element.strip() for element in row])
            # Match the block number to get the related data into the array.
            if row[0] == BlockNumber:
                offsets.append(row)
    # Close the socket.
    ifile.close()
    return offsets

# CSV writer to write offset positions of the pico projectors.
def WriteCSV(filename):
    return True

# Main loop
def main():
    print ReadCSV("offsets.csv","a1")   
    return True

if __name__ == '__main__':
    sys.exit(main())
