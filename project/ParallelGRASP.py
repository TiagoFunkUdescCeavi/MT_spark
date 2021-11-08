from multiprocessing import Manager, cpu_count
from GRASP import GRASP

class ParallelGRASP:
    def __init__(self, iterations, seed, generator, local_search, path_relinking, instance ) -> None:
        self.iterations = iterations
        self.seed = seed
        self.generator = generator
        self.local_search = local_search
        self.path_relining = path_relinking
        self.instance = instance
        self.grasps = []
        self.number_of_cpus = cpu_count()
        self.dict = Manager().dict()
    
    def __create_grasps( self ):
        for i in range( self.number_of_cpus ):
            g = GRASP( self.iterations, self.seed, self.generator, self.local_search, self.path_relining, self.instance, i, self.dict )
            self.grasps.append( g )
    
    def __start( self ):
        for g in self.grasps:
            g.start()
        
    def __join( self ):
        for g in self.grasps:
            g.join()
    
    def __select_better( self ):
        best_reward = 0.0
        best_solution = None
        for d in self.dict.values():
            if best_reward < d.get_total_rewards() :
                best_reward = d.get_total_rewards()
                best_solution = d
        return best_solution
    
    def execute( self ):
        self.__create_grasps()
        self.__start()
        self.__join()
        return self.__select_better()