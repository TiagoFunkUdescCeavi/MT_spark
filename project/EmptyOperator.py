class EmptyOperator:
    def __init__(self) -> None:
        self.unused_vertices = []

    def execute( self, solution, unused_vertices ):
        self.unused_vertices = unused_vertices
        return solution
    
    def get_unused_vertices( self ):
        return self.unused_vertices