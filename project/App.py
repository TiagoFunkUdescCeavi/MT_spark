from RandomRemoveOperator import RandomRemoveOperator
from ExchangeOperator import ExchangeOperator
from BestAddOperator import BestAddOperator
from InstanceReader import read
from RandomGreedyGen_MinMax import RandomGreedyGen_MinMax
from LocalSearch import LocalSearch
from GRASP import GRASP

class App:

    def __init__( self, argument_reader ) -> None:
        self.argument_reader = argument_reader
    
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
    
    def initialize_timer( self ):
        pass

    def create_seed( self ):
        seed = int( self.argument_reader.getValue( "--seed" ) )
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
        return operators

    def create_local_search( self ):
        return LocalSearch( self.create_operators() )
    
    def create_and_execute_grasp( self ):
        iterations = int( self.argument_reader.getValue("--iterations") )
        instance = self.read_instance()
        grasp = GRASP( iterations, self.create_seed(), self.create_solution_generator( instance ), self.create_local_search(), instance )
        return grasp.execute()
    
    def finalize_timer( self ):
        return 0
    
    def show_results( self, solution, time ):
        print( solution.to_string() )
        print( str( solution.get_total_rewards() ) )
        print( str( time ) + " ms" )
    
    def execute( self ):
        self.initialize_timer()
        solution = self.create_and_execute_grasp()
        time = self.finalize_timer()
        self.show_results( solution, time )