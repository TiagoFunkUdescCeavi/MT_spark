class BestAddOperator:

    def __init__(self) -> None:
        self.unused_vertices = []

    def realize_add( self, solution ):
        self.is_added = False
        vertice_position = -1
        best_solution = solution
        actual_solution = solution
        for i in range( solution.get_number_paths() ):
            for j in range( solution.get_length_of_path( i )-1 ):
                for k in range( len( self.unused_vertices ) ):
                    if actual_solution.add_in_path( i,j, self.unused_vertices[ k ] ):
                        if best_solution.get_total_rewards() < actual_solution.get_total_rewards():
                            self.is_added = True
                            vertice_position = k
                            best_solution = actual_solution
                        actual_solution = solution
        
        if vertice_position != -1 :
            vertice = self.unused_vertices[ vertice_position ]
            self.unused_vertices.remove( vertice )
        
        return best_solution
    
    def execute( self, solution, unused_vertices ):
        self.unused_vertices = unused_vertices #shuffle_vertices( uv )
        while True:
            solution = self.realize_add( solution )
            if not self.is_added:
                break
        return solution

    def get_unused_vertices( self ):
        return self.unused_vertices