from Solution import Solution
from Utils import truncate

class LocalSearch:
    def __init__( self, operators ) -> None:
        if len( operators ) == 0:
            raise Exception("operator list of local search is empty")
        self.operators = operators
        self.unused_vertices = []
    
    def is_better( self, actual_solution, best_solution ):
        return best_solution.get_total_rewards() < actual_solution.get_total_rewards()
    
    def is_bigger( self, sol ):
        result = False
        for i in range( sol.get_number_paths() ) :
            result = result or truncate( sol.get_time_path( i ), 2 ) > truncate( sol.get_time_per_path(), 2 )
        return result
    
    def is_shorter( self, actual_solution, best_solution ):
        result = best_solution.get_total_rewards() == actual_solution.get_total_rewards()
        result = result and truncate( actual_solution.get_total_time(), 2 ) < truncate( best_solution.get_total_rewards(), 2 )
        return result
    
    def execute( self, sol, vertices ):
        is_moved = True
        best_solution = sol
        actual_solution = sol
        self.unused_vertices = vertices

        while is_moved:
            is_moved = False

            for op in self.operators:
                actual_solution = op.execute( actual_solution, self.unused_vertices )
                self.unused_vertices = op.get_unused_vertices()
            
            is_moved = self.is_better( actual_solution, best_solution )
            is_moved = is_moved or self.is_bigger( actual_solution ) 
            is_moved = is_moved or self.is_bigger( best_solution )
            is_moved = is_moved or self.is_shorter( actual_solution, best_solution ) 
            if is_moved:
                best_solution = actual_solution
            
        return best_solution
        
    def get_unused_vertices( self ):
        return self.unused_vertices