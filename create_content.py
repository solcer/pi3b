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

# If ShowImage is set to yes, the content is created using sample input under Content folder.
# BlockNumber determines the position of the five pico projector.
def main(ShowImage='yes'):
    # Recognize Raspberry PI.
    if socket.gethostname() == 'PI3B01':
        BlockNumber           = 'a1'
        ImageCounterCoustant  = 0
    elif socket.gethostname() == 'PI3B02':
        BlockNumber           = 'a2'
        ImageCounterConstant  = 5
    # Reading offsets.csv to retrieve the offset values.
    offsets = ReadCSV("offsets.csv",BlockNumber)
    # Width, and height of the desired image.
    width         = 848
    height        = 480
    # Number of views.
    NumberOfViews = 5
    # Colors are defined.
    colors     = [
                 (255,0,0),
                 (0,255,0),
                 (0,0,255),
                 (255,255,0),
                 (255,0,255),
                 (0,255,255),
                 (100,20,50),
                 (255,255,255),
                 (127,100,0),
                 (0,255,100),
                 (0,100,127),
                 (127,127,0),
                 (127,255,127),
                 (0,127,127),
                 (200,0,50),
                 (50,255,0),
                 (100,50,100),
                 (150,150,0),
                 (0,150,150),
                 (100,200,0),
                 (0,100,200),
                 (200,0,100),
                 (100,0,200),
                 (200,100,0),
                 (50,0,255),
                 ]
    # Slit is defined geometrically.
    SlitHeight      = 20
    SlitSize        = [0, SlitHeight]
    # Load multiview images and slice them into pieces
    ImageSlices     = []
    ImageCounter    = []
    MultiViewImages = ['./Content/right.jpg','./Content/left.jpg'] 
    for ImageName in MultiViewImages:
        ImageSlices.append(LoadImage(ImageName,SlitHeight, 480, 200))
        # ImageCounter used in displaying right images.
        ImageCounter.append(ImageCounterConstant)
    # Number of slits calculated.
    NumberOfSlits = height / SlitSize[1]
    # Loop to create each view.
    for j in xrange(0,NumberOfViews):
        # Setting offset
        OffsetLeft  = int(offsets[j][2])
        OffsetTop   = int(offsets[j][3])
        SlitSize[0] = int(offsets[j][4])
        # Creating the new surface.
        NewSurface = pygame.Surface((width, height))
        # Loop to create each slit.
        for i in xrange(0,NumberOfSlits):
            slit       = pygame.Rect((OffsetLeft,(i*SlitSize[1] + OffsetTop) % height), SlitSize)
            pygame.draw.rect(NewSurface, colors[i], slit, 0)
            # If image display is desired, this if loop takes on.
            if ShowImage == 'yes':
                # Choosing the specific slices in the image for correct image registration.
                if colors[i] == (127,255,127):
                    # Adjusting image according to the image height.
                    ImageSlices[0][ImageCounter[0]] = pygame.transform.scale(ImageSlices[0][ImageCounter[0]],(SlitSize[0], SlitSize[1]))
                    # Necessary slice is being place accordingly.
                    NewSurface.blit(ImageSlices[0][ImageCounter[0]], slit)                
                    # Increasing the image counter to take right slice in the next step.
                    ImageCounter[0] += 1
                # Choosing the specific slices in the image for correct image registration.
                if colors[i] == (200,0,50):
                    # Adjusting image according to the image height.
                    ImageSlices[1][ImageCounter[1]] = pygame.transform.scale(ImageSlices[0][ImageCounter[1]],(SlitSize[0], SlitSize[1]))
                    # Necessary slice is being place accordingly.
                    NewSurface.blit(ImageSlices[1][ImageCounter[1]], slit)                
                    # Increasing the image counter to take right slice in the next step.
                    ImageCounter[1] += 1
        # Fill the blank space with correct color.
        if NewSurface.get_at((0,0)) == (0,0,0,255):
            slit       = pygame.Rect((OffsetLeft,0), (SlitSize[0], SlitSize[1]/2))
            pygame.draw.rect(NewSurface, NewSurface.get_at((width-1,height-1)), slit, 0)
        # Saving the surface as an image file.
        if j % 2 == 1 and BlockNumber == 'a1':
            NewSurface = pygame.transform.rotate(NewSurface, 180)
        if j % 2 == 0 and BlockNumber == 'a2':
            NewSurface = pygame.transform.rotate(NewSurface, 180)
        pygame.image.save(NewSurface, './Content/samplescreen%d.png' % j)
    return True

# Function to load image and slice it
def LoadImage(path,SlitHeight=20,reverse=0,width=200,height=480):
    # Image load takes place.
    Image   = pygame.image.load(path)
    # Transform the image into usable format
    Image   = pygame.transform.scale(Image,(width, height))
    # Image properties are saved.
    ImgH    = Image.get_height()
    ImgW    = Image.get_width()
    Cropped = []
    # Producing the slices.
    for i in xrange(0,ImgW/SlitHeight):   
        # Cropping takes place. 
        Cropped.append(pygame.Surface((SlitHeight,ImgH)))
        Cropped[i].blit(Image, (0,0), (i*SlitHeight,0,SlitHeight,ImgH))
        # Rotating the each slice with 90.
        Cropped[i] = pygame.transform.rotate(Cropped[i], -90)
    # Reverse ordering slices.
    if reverse == 1:
        Cropped = Cropped[::-1]
    return Cropped

if __name__ == '__main__':
    sys.exit(main('yes'))
