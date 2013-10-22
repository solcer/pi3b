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
    NumberOfViews = 2
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
    slitsize   = (width,20)
    # Number of slits calculated.
    NumberOfSlits = height / slitsize[1]
    # Loop to create each view.
    for j in xrange(0,NumberOfViews+1):
        # Start offset calculated.
        OffsetTop = j * slitsize[1]/2
        # Creating the new surface.
        NewSurface = pygame.Surface((width, height))
        # Loop to create each slit
        for i in xrange(0,NumberOfSlits):
            slit       = pygame.Rect((0,(i*slitsize[1] + OffsetTop) % height), slitsize)
            pygame.draw.rect(NewSurface, colors[i], slit, 0)
        if NewSurface.get_at((0,0)) == (0,0,0,255):
            slit       = pygame.Rect((0,0), (slitsize[0],slitsize[1]/2))
            pygame.draw.rect(NewSurface, colors[i], slit, 0)
        # Saving the surface as an image file.
        pygame.image.save(NewSurface, './Content/samplescreen%d.png' % j)
    return True

if __name__ == '__main__':
    sys.exit(main())
