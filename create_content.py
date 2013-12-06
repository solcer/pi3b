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
    # Number of views.
    NumberOfViews = 6
    # Recognize Raspberry PI.
    if socket.gethostname() == 'PI3B01':
        BlockNumber           = 'a1'
        ImageCounterConstant  = 0
    elif socket.gethostname() == 'PI3B02':
        BlockNumber           = 'a2'
        ImageCounterConstant  = NumberOfViews
    # Reading offsets.csv to retrieve the offset values.
    offsets = ReadCSV("offsets.csv",BlockNumber)
    # Width, and height of the desired image.
    width         = 848
    height        = 480
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
                 (100,150,50),
                 (0,255,150),
                 (50,100,70),
                 (0,30,200),
                 (100,100,0),
                 (40,10,23),
                 (70,80,90),
                 (138,56,190),
                 (123,23,10),
                 (234,123,34),
                 (4,4,233),
                 (23,56,12),
                 (43,34,34),
                 (43,255,34),
                 (65,45,23),
                 (90,90,56),
                 (45,122,56),
                 (230,120,42),
                 (45,45,200),
                 (80,0,255),
                 (100,200,67),
                 (200,0,34),
                 (100,250,230),
                 (45,12,32),
                 (12,99,200),
                 (234,234,53),
                 (43,89,75),
                 ]
    # Slit is defined geometrically.
    SlitHeight      = 26
    SlitSize        = [0, SlitHeight]
    # Load multiview images and slice them into pieces
    ImageSlices     = []
    ImageCounter    = []
    MultiViewImages = ['./Content/right.jpg','./Content/left.jpg'] 
    for ImageName in MultiViewImages:
        # Adding a new slice to the slices matrix.
        ImageSlices.append(LoadImage(ImageName,SlitHeight, 480, 200))
    # Number of slits calculated.
    NumberOfSlits = height / SlitSize[1] + 1
    # ImageCounter vector is built.
    for z in xrange(0,NumberOfSlits):
        # ImageCounter used in displaying right images.
        ImageCounter.append(ImageCounterConstant)
    # Flag for stereoscopic view with single perspective.
    flag          = 'left'
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
            if j == 2:
                print (i*SlitSize[1] + OffsetTop), ' ',  colors[i]
            if (i*SlitSize[1] + OffsetTop) > 0:
                slit       = pygame.Rect((OffsetLeft,(i*SlitSize[1] + OffsetTop)), SlitSize)
            else:
                slit       = pygame.Rect((OffsetLeft,((NumberOfSlits + i)*SlitSize[1] + OffsetTop)), SlitSize)
            pygame.draw.rect(NewSurface, colors[i], slit, 0)
            # If image display is desired, this if loop takes on.
            if ShowImage == 'yes':
                # Specify which color is replaced with an image.
                a = i 
                # Choosing the specific slices in the image for correct image registration.
                if flag == 'left':
                    flag        = 'right'
                    ChosenImage = ImageSlices[0]
                else:
                    flag        = 'left'
                    ChosenImage = ImageSlices[1]
                # Adjusting image according to the image height.
                ChosenImage[ImageCounter[a]] = pygame.transform.scale(ChosenImage[ImageCounter[a]],(SlitSize[0], SlitSize[1]))
                # Necessary slice is being place accordingly.
                NewSurface.blit(ChosenImage[ImageCounter[a]], slit)                
                # Increasing the image counter to take right slice in the next step.
                ImageCounter[a] += 1
        # Fill the blank space with correct color.
#        if NewSurface.get_at((0,0)) == (0,0,0,255):
#            slit       = pygame.Rect((OffsetLeft,0), (SlitSize[0], SlitSize[1]))
#            pygame.draw.rect(NewSurface, NewSurface.get_at((width-1,height-1)), slit, 0)
        # Saving the surface as an image file.
#        if j % 2 == 0 and BlockNumber == 'a2':
#            NewSurface = pygame.transform.rotate(NewSurface, 180)
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
    sys.exit(main('no'))
