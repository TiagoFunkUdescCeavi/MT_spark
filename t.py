from multiprocessing import Process, Manager

SIZE = 10000000

class Adder( Process ):
    def __init__(self, id, end, dict ) -> None:
        super( Adder, self ).__init__()
        self.id = id
        self.e = end
        self.dict = dict
    
    def run( self ):
        sum = 0
        for i in range( 1 ):
            for i in range( self.e ):
                sum += i
        self.dict[ self.id ] = sum

adders = []
dict = Manager().dict()
for i in range( 8 ):
    adders.append( Adder( i, SIZE+i, dict ) )

for a in adders:
    a.start()
    print( "start" )

for a in adders:
    a.join()
    print( "join" )

print( dict )