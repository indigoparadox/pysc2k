#!/usr/bin/env python3

import math
import logging
from pysc2k.city import SC2kCity

def main():
    logging.basicConfig( level=logging.DEBUG )
    logging.getLogger( 'chunk.rle.unpack' ).setLevel( logging.ERROR )
    logging.getLogger( 'sc2k.city.terrain.real' ).setLevel( logging.ERROR )
    logger = logging.getLogger( 'main' )
    city = SC2kCity( './iskarton.sc2' )
    height_factor = 0.5
    with open( 'out.txt', 'w' ) as out_file:
        row_sz = int( math.sqrt( len( city.tiles ) ) )
        logger.debug( '{} tiles in a row'.format( row_sz ) )
        x = 0
        y = 0
        for tile in city.tiles:
            if (height_factor * 500) > tile.altitude:
                out_file.write( '.' )
            elif (height_factor * 1000) > tile.altitude:
                out_file.write( ',' )
            elif (height_factor * 1500) > tile.altitude:
                out_file.write( '*' )
            elif (height_factor * 2000) > tile.altitude:
                out_file.write( 'o' )
            elif (height_factor * 2500) > tile.altitude:
                out_file.write( 'O' )
            elif (height_factor * 3000) > tile.altitude:
                out_file.write( '@' )
            x += 1
            if x >= row_sz:
                out_file.write( '\n' )
                x = 0
                y += 1
            

if '__main__' == __name__:
    main()

