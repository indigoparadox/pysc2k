
import logging
import struct
from chunk import Chunk

FILE_HEADER_SZ = 12
CHUNK_HEADER_SZ = 8
COMPRESSED_CHUNKS = [
    'MISC', 'XTER', 'XBLD', 'XZON', 'XUND', 'XTXT', 'XLAB', 'XMIC', 'XTHG',
    'XBIT', 'XTRF', 'XPLT', 'XVAL', 'XCRM', 'XPLC', 'XFIR', 'XPOP', 'XROG',
    'XGRP'
]

TILE_CORNERS_NONE = (0, 0, 0, 0)
TILE_CORNERS_ALL = (1, 1, 1, 1)

#                       nw  ne  sw  se
TILE_CORNERS_NW_NE =    (1, 1,  0,  0)
TILE_CORNERS_NE_SE =    (0, 1,  0,  1)
TILE_CORNERS_NE_SW =    (0, 1,  1,  0)
TILE_CORNERS_NW_SW =    (1, 0,  1,  0)
TILE_CORNERS_NW_NE_SE = (1, 1,  0,  1)
TILE_CORNERS_NE_SW_SE = (0, 1,  1,  1)
TILE_CORNERS_NW_SW_SE = (1, 0,  1,  1)
TILE_CORNERS_NW_NE_SW = (1, 1,  1,  0)
TILE_CORNERS_NE =       (0, 1,  0,  0)
TILE_CORNERS_SE =       (0, 0,  0,  1)
TILE_CORNERS_SW =       (0, 0,  1,  0)
TILE_CORNERS_NW =       (1, 0,  0,  0)

WATER_NONE =            (0, 0,  0,  0)

#                       n   e   s   w
WATER_CANAL_W_E =       (0, 1,  0,  1)
WATER_CANAL_N_S =       (1, 0,  1,  0)
WATER_BAY_N =           (1, 0,  0,  0)
WATER_BAY_E =           (0, 1,  0,  0)
WATER_BAY_S =           (0, 0,  1,  0)
WATER_BAY_W =           (0, 0,  0,  1)

class RLEChunk( object ):

    # We can't use the python inbuilt chunk because of SC2k's compression.

    def __init__( self, iff ):
        self.iff = iff
        logger = logging.getLogger( 'chunk.rle' )
        header = struct.unpack( '>4sI', self.iff.read( 8 ) )
        self.name = header[0].decode( 'utf-8' )
        self.size = header[1]
        logger.debug( 'opened chunk "{}", size: {}'.format(
            self.name, self.size ) )
        self.data = iff.read( self.size )
        assert( len( self.data ) == self.size )

    def decompress_chunk( self ):

        logger = logging.getLogger( 'chunk.rle.unpack' )
        
        master_iter = 0
        bytes_out = bytearray()
        while len( self.data ) - 1 >= master_iter:
            span_sz = self.data[master_iter]
            master_iter += 1
            span_compressed = False

            logger.debug( 'data out is {} bytes...'.format( len( bytes_out ) ) )
            
            # Is the span compressed?
            if 129 <= span_sz:
                assert( 255 >= span_sz )
                span_sz -= 127
                logger.debug(
                    'found compressed span of {} bytes at {}'.format(
                        span_sz, master_iter ) )
                span_compressed = True
            elif 127 >= span_sz:
                assert( 0 < span_sz )
                logger.debug(
                    'found span of {} bytes at {}'.format( 
                        span_sz, master_iter ) )

            # Decode the span.
            for span_iter in range( span_sz ):
                # Copy a raw span of master bytes.
                bytes_out.append( self.data[master_iter] )
                if not span_compressed:
                    master_iter += 1
            if span_compressed:
                master_iter += 1

        self.data = bytes( bytes_out )

class SC2kTile( object ):
    def __init__( self ):
        self.altitude = 0
        self.raised = TILE_CORNERS_NONE
        self.water = WATER_NONE
        self.canal = TILE_CORNERS_NONE

class SC2kCity( object ):
    
    def __init__( self, path ):

        logger = logging.getLogger( 'sc2k.city.read' )

        with open( path, 'rb' ) as city_file:

            file_header = SC2kCity._read_header( city_file )
            # You would think it would FILE_HEADER_SZ, but the number in the
            # header seems to excluse CHUNK_HEADER_SZ instead.
            city_sz = file_header[1] + CHUNK_HEADER_SZ
            logger.debug( 'opened city file {} bytes long'.format(
                city_sz ) )

            file_pos = FILE_HEADER_SZ
            city_file.seek( file_pos )

            # Iterate through chunks in the file.
            while file_pos < city_sz:
                logger.debug( 'opening chunk at {} ({})...'.format(
                    file_pos, city_sz ) )
                chunk_iter = RLEChunk( city_file )

                if chunk_iter.name in COMPRESSED_CHUNKS:
                    chunk_iter.decompress_chunk()

                logger.debug( 'chunk is {} bytes'.format(
                    len( chunk_iter.data ) ) )

                # Decode chunks into city data by chunk type.
                if 'ALTM' == chunk_iter.name:
                    self._read_alt_map( chunk_iter )

                # Move to the next chunk.
                file_pos += CHUNK_HEADER_SZ + chunk_iter.size
                city_file.seek( file_pos )

    def _read_alt_map( self, chunk ):

        logger = logging.getLogger( 'sc2k.city.tile.read' )

        tiles_sz = int( len( chunk.data ) / 2 )
        self.tiles = []

        for i in range( tiles_sz ):
            if i >= len( self.tiles ):
                self.tiles.append( SC2kTile() )
            self.tiles[i].height = (chunk.data[i] & 0xf0) >> 4
            #logger.debug( 'tile #{}: {}'.format( int( i / 2 ), self.tiles[i].height ) )

    @staticmethod
    def _read_tile_terrain( self, tile_bits ):
        pass

    @staticmethod
    def _read_header( city_file ):
        return struct.unpack( '>4sI4s', city_file.read( 12 ) )

