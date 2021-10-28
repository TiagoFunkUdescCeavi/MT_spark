from Utils import truncate

class ExchangeOperator:
    def __init__(self) -> None:
        self.is_swaped = False
        self.unused_vertices = []
    
    def realize_operation( self, solution ):
        self.is_swaped = False
        actual_solution = solution
        best_solution = solution
        for i in range( actual_solution.get_number_paths() ):
            for j in range( i+1, actual_solution.get_number_paths() ):
                for k in range( 1, actual_solution.get_length_of_path( i )-1 ):
                    for l in range( 1, actual_solution.get_length_of_path( i )-1 ):
                        if actual_solution.swap( i,k,j,l ):
                            if truncate( actual_solution.get_total_time(), 2 ) < truncate( best_solution.get_total_time(), 2 ):
                                best_solution = actual_solution
                                self.is_swaped = True
                            else:
                                actual_solution = solution
        return best_solution
    
    def execute( self, solution, unused_vertices ):
        self.unused_vertices = unused_vertices
        while True:
            solution = self.realize_operation( solution )
            if not self.is_swaped :
                break
        return solution
    
    def get_unused_vertices( self ):
        return self.unused_vertices