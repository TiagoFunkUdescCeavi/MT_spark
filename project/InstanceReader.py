from Vertice import Vertice
from Instance import Instance

def read( file ):
    arq = open( file )
    text = arq.readlines()

    line = text[ 0 ].split(" ")
    vertices = int( line[ 1 ] )

    line = text[ 1 ].split(" ")
    paths = int( line[ 1 ] )

    line = text[ 2 ].split(" ")
    time_per_path = float( line[ 1 ] )

    inst = Instance()
    inst.set_number_vertices( vertices )
    inst.set_number_paths( paths )
    inst.set_time_per_path( time_per_path )

    for i in range( 3, len( text ) ):
        line = text[ i ].split( "\t" )
        x = float( line[ 0 ] )
        y = float( line[ 1 ] )
        reward = float( line[ 2 ] )
        vert = Vertice( x, y, reward )
        inst.add_point( vert )
    
    arq.close()
    return inst