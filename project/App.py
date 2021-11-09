from RandomRemoveOperator import RandomRemoveOperator
from ExchangeOperator import ExchangeOperator
from BestAddOperator import BestAddOperator
from BestSwapOperator import BestSwapOperator
from InstanceReader import read
from RandomGreedyGen_MinMax import RandomGreedyGen_MinMax
from ParallelGRASP import ParallelGRASP
from LocalSearch import LocalSearch
from PathRelinking import PathRelinking
import time
from random import randint

class App:

    def __init__( self, argument_reader ) -> None:
        self.argument_reader = argument_reader
        self.time = 0
    
    def create_remove_operator( self ):
        argument = self.argument_reader.getValue( "--removeOperator" )
        percentage = float( self.argument_reader.getValue( "--removePercentage" ) )
        if argument == "RandomRemove":
            return RandomRemoveOperator( percentage )
        raise Exception( "Remove Operator is invalid: " + argument )
    
    def create_shuffle_operator( self ):
        argument = self.argument_reader.getValue( "--shuffleOperator" )
        if argument == "Exchange":
            return ExchangeOperator()
        raise Exception( "Shuffle Operator is invalid: " + argument )
    
    def create_add_operator( self ):
        argument = self.argument_reader.getValue( "--addOperator" )
        if argument == "BestAdd":
            return BestAddOperator()
        raise Exception( "Create Operator is invalid: " + argument )
    
    def create_swap_operator( self ):
        return BestSwapOperator()
    
    def initialize_timer( self ):
        self.time = time.time()

    def create_seed( self ):
        seed = randint(0,100000000000)#int( self.argument_reader.getValue( "--seed" ) )
        print( "seed: " + str( seed ) )
        return seed
    
    def read_instance( self ):
        file = self.argument_reader.getValue( "--file" )
        instance = read( file  )
        print( "file: " + file )
        return instance

    def create_solution_generator( self, instance ):
        alpha = float( self.argument_reader.getValue( "--alpha" ) )
        margin = float( self.argument_reader.getValue( "--margin" ) )
        return RandomGreedyGen_MinMax( alpha, margin, instance.get_number_paths(), instance.get_time_per_path(), instance )
    
    def create_operators( self ):
        operators = []
        operators.append( self.create_remove_operator() )
        operators.append( self.create_shuffle_operator() )
        operators.append( self.create_add_operator() )
        operators.append( self.create_swap_operator() )
        return operators

    def create_local_search( self ):
        return LocalSearch( self.create_operators() )
    
    def create_path_relinking( self ):
        return PathRelinking( True )
    
    def create_and_execute_grasp( self ):
        iterations = int( self.argument_reader.getValue("--iterations") )
        instance = self.read_instance()
        grasp = ParallelGRASP( iterations, self.create_seed(), self.create_solution_generator( instance ), self.create_local_search(), self.create_path_relinking(), instance )
        return grasp.execute()
    
    def finalize_timer( self ):
        return time.time() - self.time
    
    def show_results( self, solution, time ):
        #print( solution.to_string() )
        print( str( solution.get_total_rewards() ) )
        print( str( time ) )
    
    def execute( self ):
        self.initialize_timer()
        solution = self.create_and_execute_grasp()
        time = self.finalize_timer()
        self.show_results( solution, time )