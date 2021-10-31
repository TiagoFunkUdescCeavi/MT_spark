class BestSwapOperator:
    def __init__(self) -> None:
        self.unused_vertices = []
        self.is_added = False
    
    def realize_swap( self, solution ):
        self.is_added = False
        best = solution
        actual = solution
        for i in range( actual.get_number_paths() ):
            for j in range( 1, actual.get_length_of_path( i )-1 ):
                for k in range( len( self.unused_vertices ) ):
                    old_vertice = actual.get_vertice_in_path( i, j )
                    new_vertice = self.unused_vertices[ k ]
                    if actual.rewrite( i, j, new_vertice ):
                        if best.get_total_rewards() < actual.get_total_rewards():
                            best = actual
                            self.unused_vertices[ k ] = old_vertice
                            self.is_added = True
                        actual = solution
        return best
    
    def execute( self, solution, unused_vertices ):
        self.unused_vertices = unused_vertices
        while True:
            solution = self.realize_swap( solution )
            if not self.is_added:
                break
        return solution
    
    def get_unused_vertices( self ):
        return self.unused_vertices