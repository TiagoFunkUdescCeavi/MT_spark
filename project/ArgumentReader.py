import sys
from typing_extensions import Final

class ArgumentReader:

    def __init__(self, args) -> None:
        if len( args ) == 1:
            raise Exception("argument list of program is empty")
        self.arguments = {}
        self.__JUMP: Final = 2
        self.__FIRST_POSITION: Final = 1
        self.__process( args )
        
    def __process( self, args ):
        for i in range( self.__FIRST_POSITION, len( args ), self.__JUMP ):
            self.arguments[ args[ i ] ] = args[ i+1 ]

    def getValue( self, name ):
        result = self.arguments.get( name )
        if result == None:
            raise Exception( "argument \"" + name + "\" not found in arguments of program")
        return result