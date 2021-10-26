from math import pow, sqrt

def calculate_distance( vertice_1, vertice_2 ):
    x_diff = vertice_2.get_x() - vertice_1.get_x()
    y_diff = vertice_2.get_y() - vertice_1.get_y()
    return sqrt( pow( x_diff, 2 ) + pow( y_diff, 2 ) )

def find_min_max( values ):
    min = values[ 0 ]
    max = values[ 0 ]
    for i in range( len( values ) ):
        if min > values[ i ]:
            min = values[ i ]
        elif max < values[ i ]:
            max = values[ i ]
    return min, max