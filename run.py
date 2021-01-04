#!/usr/bin/env python3

import logging
from pysc2k.city import SC2kCity

def main():
    logging.basicConfig( level=logging.DEBUG )
    logging.getLogger( 'chunk.rle.unpack' ).setLevel( logging.ERROR )
    city = SC2kCity( './iskarton.sc2' )

if '__main__' == __name__:
    main()

