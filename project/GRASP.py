from RandomGreedyGen_MinMax import RandomGreedyGen_MinMax
from Solution import Solution

class GRASP:
    def __init__( self, iterations, seed, generator, instance ) -> None:
        self.iterations = iterations
        self.seed = seed
        self.generator = generator
        self.instance = instance
        self.unused_vertices = []
    
    def generate( self ):
        self.unused_vertices.clear()
        sol = self.generator.generate( self.instance.get_vertices_on_path() )
        self.unused_vertices = self.generator.get_unused_vertices()
        return sol
    
    def is_accepted( self, sol ):
        return True
    
    def is_better( self, actual_solution, best_solution ):
        return actual_solution.get_total_rewards() > best_solution.get_total_rewards()
    
    def execute( self ):
        first_iteration = True
        #set seed on rng
        for i in range( self.iterations ):
            actual_solution = self.generate()

            if not self.is_accepted( actual_solution ):
                continue
            
            if first_iteration:
                best_solution = actual_solution
                first_iteration = False

            if self.is_better( actual_solution, best_solution):
                best_solution = actual_solution
                print( str( i+1 ) + " " + str( best_solution.get_total_rewards() ) + "\n")
        
        return best_solution



