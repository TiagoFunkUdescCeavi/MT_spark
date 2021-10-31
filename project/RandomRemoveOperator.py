from random import *

class RandomRemoveOperator:
    def __init__(self, percentage ) -> None:
        self.unused_vertices = []
        self.percentage = percentage

    def random_path( self, solution ):
        numbers = []
        for i in range( solution.get_number_paths() ):
            if not solution.is_empty( i ):
                numbers.append( i )
        
        for i in range( len( numbers ) ):
            position = randint( 0, len( numbers ) - 1 )
            swap = numbers[ position ]
            numbers[ position ] = numbers[ i ]
            numbers[ i ] = swap
        
        if len( numbers ) == 0:
            return -1
        return numbers[ 0 ]
    
    def remove( self, solution ):
        path = self.random_path( solution )
        if path == -1:
            solution
        actual_solution = solution
        position = randint( 1, actual_solution.get_length_of_path( path ) - 2 )
        vertice = actual_solution.get_vertice_in_path( path, position )
        actual_solution.remove( path, position )
        self.unused_vertices.append( vertice )
        return actual_solution
    
    def execute( self, solution, unused_vertices ):
        self.unused_vertices = unused_vertices
        total_length = solution.get_total_length_of_path()
        if total_length != 0 :
            total_length = int( total_length * self.percentage ) + 1
            for i in range( total_length ):
                solution = self.remove( solution )
        return solution
    
    def get_unused_vertices( self ):
        return self.unused_vertices