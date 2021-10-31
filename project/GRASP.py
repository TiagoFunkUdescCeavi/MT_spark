from RandomGreedyGen_MinMax import RandomGreedyGen_MinMax
from random import seed

class GRASP:
    def __init__( self, iterations, seed, generator, local_search, path_relinking, instance ) -> None:
        self.iterations = iterations
        self.seed = seed
        self.generator = generator
        self.local_search = local_search
        self.path_relining = path_relinking
        self.instance = instance
        self.unused_vertices = []
    
    def generate( self ):
        self.unused_vertices.clear()
        sol = self.generator.generate( self.instance.get_vertices_on_path() )
        sol.update_time_per_path( self.instance.get_time_per_path() )
        self.unused_vertices = self.generator.get_unused_vertices()
        return sol

    def apply_local_search( self, solution ):
        actual_solution = self.local_search.execute( solution, self.unused_vertices )
        self.unused_vertices = self.local_search.get_unused_vertices()
        return actual_solution
    
    def apply_path_relinking( self, solution, best_solution ):
        if best_solution == None or best_solution.get_total_time() == 0.0:
            return solution
        return self.path_relining.execute( solution, best_solution )
    
    def is_accepted( self, sol ):
        return True
    
    def is_better( self, actual_solution, best_solution ):
        if actual_solution == None and best_solution == None:
            raise RuntimeError("both variables are None")
        if actual_solution == None:
            raise RuntimeError("actual_solution are None")
        if best_solution == None:
            return True
        return actual_solution.get_total_rewards() > best_solution.get_total_rewards()
    
    def execute( self ):
        actual_solution = None
        best_solution = None
        seed( self.seed )

        for i in range( self.iterations ):
            actual_solution = self.generate()

            if not self.is_accepted( actual_solution ):
                continue
            
            actual_solution = self.apply_local_search( actual_solution )

            actual_solution = self.apply_path_relinking( actual_solution, best_solution )

            if self.is_better( actual_solution, best_solution):
                best_solution = actual_solution
                print( str( i+1 ) + " " + str( best_solution.get_total_rewards() ) )
        
        return best_solution



