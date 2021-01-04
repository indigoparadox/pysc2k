#!/usr/bin/env python3

import math
import logging
from pysc2k.city import SC2kCity, TILE_DRY

def main():
    logging.basicConfig( level=logging.DEBUG )
    logging.getLogger( 'chunk.rle.unpack' ).setLevel( logging.ERROR )
    logging.getLogger( 'sc2k.city.terrain.real' ).setLevel( logging.ERROR )
    logger = logging.getLogger( 'main' )
    city = SC2kCity( './iskarton.sc2' )
    height_factor = 0.05
    with open( 'out.txt', 'w' ) as out_file:
        row_sz = int( math.sqrt( len( city.tiles ) ) )
        logger.debug( '{} tiles in a row'.format( row_sz ) )
        x = 0
        y = 0
        for tile in city.tiles:
            if tile.water:
                out_file.write( 'w' )
            elif TILE_DRY != tile.submerged:
                out_file.write( 'W' )
            elif (height_factor * 0x2a) > tile.altitude:
                out_file.write( '.' )
            elif (height_factor * 0x54) > tile.altitude:
                out_file.write( ',' )
            elif (height_factor * 0x7e) > tile.altitude:
                out_file.write( '*' )
            elif (height_factor * 0xa8) > tile.altitude:
                out_file.write( 'o' )
            elif (height_factor * 0xd2) > tile.altitude:
                out_file.write( 'O' )
            elif (height_factor * 0xfc) > tile.altitude:
                out_file.write( '@' )
            x += 1
            if x >= row_sz:
                out_file.write( '\n' )
                x = 0
                y += 1
            

if '__main__' == __name__:
    main()

