class ExchangeOperator:
    def __init__(self) -> None:
        self.is_swaped = False
        self.unused_vertices = []
    
    def realize_operation( self, solution ):
        self.is_swaped = False
        actual_solution = solution
        best_solution = solution
        for path1 in range( actual_solution.get_number_paths() ):
            for path2 in range( path1+1, actual_solution.get_number_paths() ):
                for position1 in range( 1, actual_solution.get_length_of_path( path1 )-1 ):
                    for position2 in range( 1, actual_solution.get_length_of_path( path2 )-1 ):
                        if actual_solution.swap( path1, position1, path2, position2 ):
                            if actual_solution.get_total_time() < best_solution.get_total_time():
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