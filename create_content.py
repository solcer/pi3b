#!/usr/bin/python
# -*- coding: utf-8 -*-

__author__ = ('Kaan Akşit')

import sys,os,time,pygame
from pygame.locals import *

def main():
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
    slitheight = 20
    slitsize   = (0, slitheight)
    # Number of slits calculated.
    NumberOfSlits = height / slitsize[1]
    # Loop to create each view.
    for j in xrange(0,NumberOfViews):
        # Setting offset
        if j % 2 == 1:
           if j == 1:
               OffsetTop  = 68 * slitsize[1]/4
               OffsetLeft = 0 
               slitwidth  = width
           if j == 3:
               OffsetTop  = 66 * slitsize[1]/4            
               OffsetLeft = 0 
               slitwidth  = width
        else:
           if j == 0:
               OffsetTop  = 0
               OffsetLeft = 20 
               slitwidth  = width
           if j == 2:
               OffsetTop  = - 3 * slitsize[1]/4
               OffsetLeft = 0 
               slitwidth  = width - 20
           if j == 4:
               OffsetTop  = - 5 * slitsize[1]/4
               OffsetLeft = 0 
               slitwidth  = width
        # Creating the new surface.
        NewSurface = pygame.Surface((width, height))
        # Loop to create each slit
        for i in xrange(0,NumberOfSlits):
            slit       = pygame.Rect((OffsetLeft,(i*slitsize[1] + OffsetTop) % height), slitsize)
            pygame.draw.rect(NewSurface, colors[i], slit, 0)
        # Fill the blank space with correct color.
        if NewSurface.get_at((0,0)) == (0,0,0,255):
            slit       = pygame.Rect((OffsetLeft,0), (slitsize[0], slitsize[1]/2))
            pygame.draw.rect(NewSurface, NewSurface.get_at((width-1,height-1)), slit, 0)
        # Saving the surface as an image file.
        if j % 2 == 1:
            NewSurface = pygame.transform.rotate(NewSurface, 180)
        pygame.image.save(NewSurface, './Content/samplescreen%d.png' % j)
    return True

if __name__ == '__main__':
    sys.exit(main())
